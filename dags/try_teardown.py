import pendulum
from airflow.decorators import task, task_group
from airflow.operators.bash import BashOperator
from airflow.models.dag import DAG

with DAG(dag_id="s_t_dag", start_date=pendulum.datetime(2020, 1, 1), catchup=False) as dag:

    @task
    def test_task():
        print("Hello world!")

    @task_group
    def inner():
        inner_start = BashOperator(task_id="start", bash_command="sleep 10; echo 'hello'")
        inner_end = BashOperator(task_id="end", bash_command="sleep 10; echo 'hello'")
        test_task_r = test_task.override(task_id="work")()
        inner_start >> test_task_r >> inner_end.as_teardown(setups=inner_start)

    @task_group
    def outer():
        outer_work = BashOperator(task_id="work", bash_command="sleep 10; echo 'hello'")
        inner_group = inner()
        inner_group >> outer_work

    dag_start = BashOperator(task_id="dag_start", bash_command="sleep 10; echo 'hello'")
    dag_end = BashOperator(task_id="dag_end", bash_command="sleep 10; echo 'hello'")
    dag_start >> outer() >> dag_end
