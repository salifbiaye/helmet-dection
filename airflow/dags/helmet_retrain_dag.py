from datetime import datetime, timedelta
from airflow import DAG
# pyrefly: ignore [missing-import]
from airflow.operators.python import PythonOperator
# pyrefly: ignore [missing-import]
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
    description='Réentraînement hebdomadaire YOLOv8 casques',
    schedule_interval='@weekly',
    catchup=False,
    tags=['ml', 'yolo', 'helmet'],
)


def check_new_data(**kwargs):
    data_dir = '/opt/airflow/data/new_annotations'
    if os.path.exists(data_dir):
        files = os.listdir(data_dir)
        print(f'Nouvelles annotations: {len(files)}')
        return len(files) > 0
    return False


def retrain_model(**kwargs):
    from ultralytics import YOLO
    model = YOLO('/opt/airflow/models/helmet_model_best.pt')
    results = model.train(
        data='/opt/airflow/data/data.yaml',
        epochs=10,
        imgsz=640,
        batch=16,
        name='retrain',
        project='/opt/airflow/runs',
        device='cpu',
    )
    print(f'Réentraînement terminé: {results.results_dict}')


def deploy_model(**kwargs):
    import shutil
    # YOLO génère toujours le fichier sous le nom 'best.pt'
    best = '/opt/airflow/runs/retrain/weights/best.pt'
    # Mais nous voulons le copier et le renommer en 'helmet_model_best.pt'
    target = '/opt/airflow/models/helmet_model_best.pt'
    if os.path.exists(best):
        shutil.copy(best, target)
        print(f'Modèle déployé: {target}')
    else:
        raise FileNotFoundError(f'Modèle non trouvé: {best}')


check_data = PythonOperator(task_id='check_new_data', python_callable=check_new_data, dag=dag)
retrain = PythonOperator(task_id='retrain_model', python_callable=retrain_model, dag=dag)
deploy = PythonOperator(task_id='deploy_model', python_callable=deploy_model, dag=dag)
restart_api = BashOperator(
    task_id='restart_api',
    bash_command='curl -X POST http://backend:8000/admin/reload 2>/dev/null || echo "reload skipped"',
    dag=dag,
)

check_data >> retrain >> deploy >> restart_api
