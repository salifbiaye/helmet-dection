from datetime import datetime, timedelta
from airflow import DAG
# pyrefly: ignore [missing-import]
from airflow.operators.python import PythonOperator, ShortCircuitOperator
from airflow.operators.bash import BashOperator
import os

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2025, 1, 1),
    'email_on_failure': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'helmet_detection_retrain',
    default_args=default_args,
    description='Reentrainement hebdomadaire YOLOv8 casques',
    schedule_interval='@weekly',
    catchup=False,
    tags=['ml', 'yolo', 'helmet'],
)


def check_new_data(**kwargs):
    # Chemin interne au conteneur Airflow
    data_dir = '/opt/airflow/data/new_annotations'
    if os.path.exists(data_dir):
        files = [f for f in os.listdir(data_dir) if f.endswith(('.jpg', '.png', '.txt'))]
        print(f'Nouvelles données détectées : {len(files)} fichiers.')
        return len(files) > 0
    print('Dossier de données non trouvé ou vide.')
    return False


def retrain_model(**kwargs):
    from ultralytics import YOLO
    # On charge le modèle actuel pour faire du fine-tuning supplémentaire
    model = YOLO('/opt/airflow/models/helmet_model_best.pt')
    results = model.train(
        data='/opt/airflow/data/data.yaml',
        epochs=5,  # On fait peu d'époques pour le réentraînement auto
        imgsz=640,
        batch=8,
        name='retrain',
        project='/opt/airflow/runs',
        device='cpu', # Force CPU pour éviter les erreurs si pas de GPU Docker
    )
    print(f'Reentrainement termine avec succès.')


def deploy_model(**kwargs):
    import shutil
    # YOLO génère le meilleur poids dans weights/best.pt
    best = '/opt/airflow/runs/retrain/weights/best.pt'
    target = '/opt/airflow/models/helmet_model_best.pt'
    if os.path.exists(best):
        shutil.copy(best, target)
        print(f'Nouveau modèle déployé vers : {target}')
    else:
        raise FileNotFoundError(f'Fichier best.pt non trouvé à {best}')


# Utilisation du ShortCircuitOperator : si renvoie False, la suite du DAG est ignorée (skip)
check_data = ShortCircuitOperator(
    task_id='check_new_data',
    python_callable=check_new_data,
    dag=dag
)

retrain = PythonOperator(
    task_id='retrain_model',
    python_callable=retrain_model,
    dag=dag
)
deploy = PythonOperator(task_id='deploy_model', python_callable=deploy_model, dag=dag)
restart_api = BashOperator(
    task_id='restart_api',
    bash_command='curl -X POST http://backend:8000/admin/reload 2>/dev/null || echo "reload skipped"',
    dag=dag,
)

check_data >> retrain >> deploy >> restart_api
