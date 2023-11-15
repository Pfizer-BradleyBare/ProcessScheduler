# Copyright (c) 2020-2021 Thomas Paviot (tpaviot@gmail.com)
#
# This file is part of ProcessScheduler.
#
# This program is free software: you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software
# Foundation, either version 3 of the License, or (at your option) any later
# version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
# You should have received a copy of the GNU General Public License along with
# this program. If not, see <http://www.gnu.org/licenses/>.

import json

import processscheduler as ps

import pytest


# the same temp path in all the module
@pytest.fixture(scope="module", autouse=True)
def my_tmp_path(tmp_path_factory):
    return tmp_path_factory.mktemp("mon_dossier_temporaire")


a_problem = ps.SchedulingProblem(name="JSONExportProblem1", horizon=10)


# tasks
def test_FixedDurationTask_to_json_file(my_tmp_path):
    ps.SchedulingProblem(name="FixedDurationTaskToJson")
    ps.FixedDurationTask(name="T_fixed", duration=3).to_json_file(
        my_tmp_path / "fixed_duration_task.json"
    )


def test_FixedDurationTask_from_json(my_tmp_path):
    ps.SchedulingProblem(name="FixedDurationTaskFromJson")
    with open(my_tmp_path / "fixed_duration_task.json", "r") as f:
        t = ps.FixedDurationTask.model_validate_json(f.read())
    assert t.name == "T_fixed"
    assert not t.optional
    assert t.duration == 3
    assert t.priority == 0
    assert t.work_amount == 0


def test_ZeroDurationTask_to_json_file(my_tmp_path):
    ps.SchedulingProblem(name="ZeroDurationTaskToJson")
    ps.ZeroDurationTask(name="T_zero").to_json_file(
        my_tmp_path / "zero_duration_task.json"
    )


def test_ZeroDurationTask_from_json(my_tmp_path):
    ps.SchedulingProblem(name="ZeroDurationTaskFromJson")
    with open(my_tmp_path / "zero_duration_task.json", "r") as f:
        t = ps.ZeroDurationTask.model_validate_json(f.read())
    assert t.name == "T_zero"
    assert not t.optional
    assert t.duration == 0
    assert t.priority == 0
    assert t.work_amount == 0


def test_VariableDurationTask_to_json_file(my_tmp_path):
    ps.SchedulingProblem(name="VariableDurationTaskToJson")
    ps.VariableDurationTask(name="T_variable").to_json_file(
        my_tmp_path / "variable_duration_task.json"
    )


def test_VariableDurationTask_from_json(my_tmp_path):
    ps.SchedulingProblem(name="VariableDurationTaskFromJson")
    with open(my_tmp_path / "variable_duration_task.json", "r") as f:
        t = ps.VariableDurationTask.model_validate_json(f.read())
    assert t.name == "T_variable"
    assert not t.optional
    assert t.priority == 0
    assert t.work_amount == 0


# workers
def test_Worker_to_json_file(my_tmp_path):
    ps.SchedulingProblem(name="WorkerToJson")
    ps.Worker(name="W1", productivity=3).to_json_file(my_tmp_path / "worker_W1.json")


def test_Worker_from_json(my_tmp_path):
    ps.SchedulingProblem(name="WorkerFromJson")
    with open(my_tmp_path / "worker_W1.json", "r") as f:
        w = ps.Worker.model_validate_json(f.read())
    assert w.name == "W1"
    assert w.productivity == 3
    assert w.cost is None


def test_Worker_from_json_2():
    ps.SchedulingProblem(name="WorkerFromJson2")
    w = ps.Worker.model_validate_json(
        '{"name": "W2", "type": "Worker", "productivity": 1, "cost": null}'
    )
    assert w.name == "W2"
    assert w.productivity == 1
    assert w.cost is None


def test_CumulativeWorker_to_json_file(my_tmp_path):
    ps.CumulativeWorker(name="CW1", productivity=3, size=12).to_json_file(
        my_tmp_path / "cumulative_worker_W1.json"
    )


def test_CumulativeWorker_from_json(my_tmp_path):
    ps.SchedulingProblem(name="CumulativeWorkerFromJson")
    with open(my_tmp_path / "cumulative_worker_W1.json", "r") as f:
        cw = ps.CumulativeWorker.model_validate_json(f.read())
    assert cw.name == "CW1"
    assert cw.productivity == 3
    assert cw.size == 12
    assert cw.cost is None


def test_SelectWorkers_to_json_file(my_tmp_path):
    ps.SchedulingProblem(name="SelectWorkersToJson")
    w1 = ps.Worker(name="W1")
    w2 = ps.Worker(name="W2")
    w3 = ps.Worker(name="W3")
    sw = ps.SelectWorkers(list_of_workers=[w1, w2, w3], nb_workers_to_select=2)
    sw.to_json_file(my_tmp_path / "select_workers.json")


def test_SelectWorkers_from_json(my_tmp_path):
    ps.SchedulingProblem(name="SelectWorkersFromJson")
    # to build a select workers, first read
    with open(my_tmp_path / "select_workers.json", "r") as f:
        sw = json.loads(f.read())
    # first create the workers
    l_o_w = [ps.Worker.model_validate(w) for w in sw["list_of_workers"]]


def test_Problem_add_from_json():
    pb = ps.SchedulingProblem(name="ProblemAddFromJson")
    pb.add_from_json(
        '{"name": "W2", "type": "Worker", "productivity": 1, "cost": null}'
    )


def test_Problem_add_from_json_unknown_object():
    pb = ps.SchedulingProblem(name="ProblemAddFromJsonUnknownObject")
    with pytest.raises(AssertionError):
        pb.add_from_json(
            '{"name": "W2", "type": "ClassThatDoesNotExist", "productivity": 1, "cost": null}'
        )


def test_Problem_add_from_json_file(my_tmp_path):
    pb = ps.SchedulingProblem(name="ProblemAddFromJsonFile")
    t = pb.add_from_json_file(my_tmp_path / "fixed_duration_task.json")


def test_json_export_problem_solver_1(my_tmp_path):
    pb = ps.SchedulingProblem(name="JSONExportProblem1", horizon=1)
    # tasks
    task_1 = ps.FixedDurationTask(name="task1", duration=3)
    task_2 = ps.VariableDurationTask(name="task2")
    task_3 = ps.ZeroDurationTask(name="task3")

    # buffers
    buffer_1 = ps.NonConcurrentBuffer(name="Buffer1", initial_state=10)
    buffer_2 = ps.NonConcurrentBuffer(name="Buffer2", initial_state=0)

    # resources
    worker_1 = ps.Worker(name="Worker1")
    worker_2 = ps.Worker(name="Worker2")
    worker_3 = ps.Worker(name="Worker3")

    sw_1 = ps.SelectWorkers(list_of_workers=[worker_1, worker_2, worker_3])
    sw_2 = ps.SelectWorkers(list_of_workers=[worker_1, worker_2, worker_3])
    sw_3 = ps.SelectWorkers(list_of_workers=[worker_1, worker_2, worker_3])

    ps.CumulativeWorker(name="CumulMachine1", size=3)
    ps.CumulativeWorker(name="CumulMachine2", size=7)

    # assign resources to tasks
    task_1.add_required_resources([worker_1, worker_2])
    task_2.add_required_resource(sw_1)
    task_3.add_required_resource(sw_2)

    # task constraints
    ps.TaskPrecedence(task_before=task_1, task_after=task_2)
    ps.TaskStartAt(task=task_1, value=5)
    ps.TaskUnloadBuffer(task=task_1, buffer=buffer_1, quantity=3)
    ps.TaskLoadBuffer(task=task_1, buffer=buffer_2, quantity=2)

    # resource constraints
    ps.SameWorkers(select_workers_1=sw_1, select_workers_2=sw_2)
    ps.DistinctWorkers(select_workers_1=sw_2, select_workers_2=sw_3)
    ps.WorkLoad(
        resource=worker_1,
        dict_time_intervals_and_bound={(0, 6): 3, (19, 24): 4},
        kind="exact",
    )
    ps.ResourceUnavailable(resource=worker_1, list_of_time_intervals=[(1, 3), (6, 8)])
    ps.ResourceTasksDistance(
        resource=worker_1,
        distance=4,
        mode="exact",
        list_of_time_intervals=[[10, 18]],
    )

    pb.to_json(compact=True)
    pb.to_json_file(my_tmp_path / "problem.json")
    # export to json
    solver = ps.SchedulingSolver(problem=pb)
    solver.to_json()
    pb.to_json_file(my_tmp_path / "solver.json")
