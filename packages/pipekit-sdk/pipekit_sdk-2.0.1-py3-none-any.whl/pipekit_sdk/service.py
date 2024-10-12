"""Provides the PipekitService class for interacting with the Pipekit API."""

import json
import os
from typing import Any, Generator, Optional, cast

import requests
from hera.workflows import CronWorkflow, Workflow
from hera.workflows.models import WorkflowCreateRequest

from pipekit_sdk._helpers import is_valid_uuid
from pipekit_sdk.models.model import Cluster, Logs, Pipe, PipeRun


class PipekitService:
    """PipekitService is a wrapper around the Pipekit API. It provides a simple interface to interact with Pipekit."""

    def __init__(
        self,
        username: str = "",
        password: str = "",
        token: str = "",
        pipekit_url: str = "https://api.pipekit.io",
    ):
        """Initialise the service connection with the given username and password."""
        self.username = username
        self.password = password

        pipekit_url = os.getenv("PIPEKIT_URL", pipekit_url)
        if pipekit_url.endswith("/"):
            pipekit_url = pipekit_url[:-1]

        self.id_url = pipekit_url
        self.users_url = pipekit_url
        self.ui_url = pipekit_url

        if token != "":
            self.access_token = token
            return

        self.__login()

    def __login(self) -> None:
        login_request = {
            "username": self.username,
            "password": self.password,
            "grant_type": "password",
        }

        if "@" in self.username:
            login_request["email"] = self.username
            login_request["username"] = ""

        login_url = f"{self.id_url}/api/id/v1/oauth/token"
        login_response = requests.post(
            login_url,
            data=json.dumps(login_request),
            headers={"Content-Type": "application/json"},
            timeout=10,
        )

        if login_response.status_code // 100 != 2:
            raise Exception(f"Login failed: {login_response.text}")

        self.access_token = cast(str, login_response.json()["access_token"])

    def get_token(self) -> str:
        """get_token returns the access token used to authenticate with Pipekit."""
        return self.access_token

    def list_clusters(self) -> list[Cluster]:
        """Get a list of all clusters."""
        clusters_url = f"{self.users_url}/api/users/v1/clusters"
        clusters_response = requests.get(
            clusters_url,
            headers={"Authorization": f"Bearer {self.access_token}"},
            timeout=10,
        )

        if clusters_response.status_code // 100 != 2:
            raise Exception(f"List clusters failed: {clusters_response.text}")

        clusters = [Cluster.model_validate(cluster) for cluster in clusters_response.json()]
        return clusters

    def list_pipes(
        self,
        cluster_uuid: str = "",
    ) -> list[Pipe]:
        """Get a list of all pipes."""
        page = 1
        limit = 20

        pipes = []
        while True:
            pipes_url = f"{self.users_url}/api/users/v1"
            if cluster_uuid != "":
                pipes_url += f"/clusters/{cluster_uuid}"
            pipes_url += f"/pipes?page={page}&limit={limit}"

            pipes_response = requests.get(
                pipes_url,
                headers={"Authorization": f"Bearer {self.access_token}"},
                timeout=10,
            )

            if pipes_response.status_code // 100 != 2:
                raise Exception(f"List pipes failed: {pipes_response.text}")

            pipes_page = [Pipe.model_validate(item) for item in pipes_response.json()["items"]]
            if len(pipes_page) == 0:
                break

            pipes.extend(pipes_page)

            if len(pipes_page) < limit:
                break

            page += 1

        return pipes

    def get_pipe(
        self,
        pipe_uuid: str,
    ) -> Pipe:
        """Get a single pipe using its uuid."""
        pipe_url = f"{self.users_url}/api/users/v1/pipes/{pipe_uuid}"
        pipe_response = requests.get(
            pipe_url,
            headers={"Authorization": f"Bearer {self.access_token}"},
            timeout=10,
        )

        if pipe_response.status_code // 100 != 2:
            raise Exception(f"Get pipe failed: {pipe_response.text}")

        return Pipe.model_validate(pipe_response.json())

    def list_runs_by_cluster(
        self,
        cluster_uuid: str,
        status: str = "",
    ) -> list[PipeRun]:
        """Get a list of PipeRuns on a cluster using the cluster uuid."""
        page = 1
        limit = 20

        base_url = f"{self.users_url}/api/users/v1/clusters/{cluster_uuid}/runs"
        runs = []
        while True:
            runs_url = f"{base_url}?page={page}&limit={limit}&status={status}"

            runs_response = requests.get(
                runs_url,
                headers={"Authorization": f"Bearer {self.access_token}"},
                timeout=10,
            )

            if runs_response.status_code // 100 != 2:
                raise Exception(f"List runs failed: {runs_response.text}")

            runs_page = [PipeRun.model_validate(item) for item in runs_response.json()["items"]]
            if len(runs_page) == 0:
                break

            runs.extend(runs_page)

            if len(runs_page) < limit:
                break

            page += 1

        return runs

    def list_runs_by_pipe(
        self,
        pipe_uuid: str,
        status: str = "",
    ) -> list[PipeRun]:
        """Get a list of runs for a pipe using the pipe's uuid."""
        page = 1
        limit = 20

        base_url = f"{self.users_url}/api/users/v1/pipes/{pipe_uuid}/runs"
        runs = []
        while True:
            runs_url = f"{base_url}?page={page}&limit={limit}&status={status}"

            runs_response = requests.get(
                runs_url,
                headers={"Authorization": f"Bearer {self.access_token}"},
                timeout=10,
            )

            if runs_response.status_code // 100 != 2:
                raise Exception(f"List runs failed: {runs_response.text}")

            runs_page = [PipeRun.model_validate(item) for item in runs_response.json()["items"]]
            if len(runs_page) == 0:
                break

            runs.extend(runs_page)

            if len(runs_page) < limit:
                break

            page += 1

        return runs

    def get_run(
        self,
        run_uuid: str,
    ) -> PipeRun:
        """Get a PipeRun by its uuid."""
        run_url = f"{self.users_url}/api/users/v1/runs/{run_uuid}"
        run_response = requests.get(
            run_url,
            headers={"Authorization": f"Bearer {self.access_token}"},
            timeout=10,
        )

        if run_response.status_code // 100 != 2:
            raise Exception(f"Get run failed: {run_response.text}")

        return PipeRun.model_validate(run_response.json())

    def get_cluster(
        self,
        cluster_uuid: str,
    ) -> Cluster:
        """Get a single Cluster by its uuid."""
        cluster_url = f"{self.users_url}/api/users/v1/clusters/{cluster_uuid}"
        cluster_response = requests.get(
            cluster_url,
            headers={"Authorization": f"Bearer {self.access_token}"},
            timeout=10,
        )

        if cluster_response.status_code // 100 != 2:
            raise Exception(f"Get cluster failed: {cluster_response.text}")

        return Cluster.model_validate(cluster_response.json())

    def get_cluster_by_name(
        self,
        cluster_name: str,
    ) -> Optional[Cluster]:
        """Get a single Cluster by its name."""
        clusters = self.list_clusters()
        for cluster in clusters:
            if cluster.name == cluster_name:
                return cluster

        return None

    def submit(
        self,
        workflow: Workflow,
        cluster: str,
        pipe_name: str = "",
    ) -> PipeRun:
        """Submit a Workflow to a cluster, under an existing or new pipe with the given name."""
        if not is_valid_uuid(cluster):
            if cluster_obj := self.get_cluster_by_name(cluster):
                cluster = cluster_obj.uuid
            else:
                raise ValueError(f"No cluster found for {cluster}")

        submit_url = f"{self.users_url}/api/users/v1/clusters/{cluster}/workflows"
        if pipe_name != "":
            submit_url += f"?pipe-name={pipe_name}"

        model_workflow = WorkflowCreateRequest(workflow=workflow.build()).workflow  # type: ignore
        assert model_workflow is not None

        submit_response = requests.post(
            submit_url,
            data=model_workflow.json(
                exclude_none=True,
                by_alias=True,
                exclude_unset=True,
                exclude_defaults=True,
            ),
            headers={
                "Authorization": f"Bearer {self.access_token}",
                "Content-Type": "application/json",
            },
            timeout=10,
        )

        if submit_response.status_code // 100 != 2:
            raise Exception(f"Submit failed: {submit_response.text}")

        return PipeRun.model_validate(submit_response.json())

    def create(self, cron_workflow: CronWorkflow, cluster: str, pipe_name: str = "") -> PipeRun:
        """Create a CronWorkflow on the cluster, under an existing or new pipe with the given name."""
        if not is_valid_uuid(cluster):
            if cluster_obj := self.get_cluster_by_name(cluster):
                cluster = cluster_obj.uuid
            else:
                raise ValueError(f"No cluster found for {cluster}")

        create_url = f"{self.users_url}/api/users/v1/clusters/{cluster}/cron-workflows"
        if pipe_name != "":
            create_url += f"?pipe-name={pipe_name}"

        model_workflow = cron_workflow.build()
        assert model_workflow is not None

        create_response = requests.post(
            create_url,
            data=model_workflow.json(
                exclude_none=True,
                by_alias=True,
                exclude_unset=True,
                exclude_defaults=True,
            ),
            headers={
                "Authorization": f"Bearer {self.access_token}",
                "Content-Type": "application/json",
            },
            timeout=10,
        )

        if create_response.status_code // 100 != 2:
            raise Exception(f"Create failed: {create_response.text}")

        return PipeRun.model_validate(create_response.json())

    def __apply_run_action(
        self,
        run_uuid: str,
        action: str,
    ) -> PipeRun:
        action_url = f"{self.users_url}/api/users/v1/runs/{run_uuid}/workflows/{action}"
        action_response = requests.put(
            action_url,
            headers={
                "Authorization": f"Bearer {self.access_token}",
                "Content-Type": "application/json",
            },
            timeout=10,
        )

        if action_response.status_code // 100 != 2:
            raise Exception(f"Action failed: {action_response.text}")

        return PipeRun.model_validate(action_response.json())

    def restart(
        self,
        run_uuid: str,
    ) -> PipeRun:
        """Restart a run."""
        return self.__apply_run_action(run_uuid, "restart")

    def stop(
        self,
        run_uuid: str,
    ) -> PipeRun:
        """Stop a run."""
        return self.__apply_run_action(run_uuid, "stop")

    def terminate(
        self,
        run_uuid: str,
    ) -> PipeRun:
        """Terminate a run."""
        return self.__apply_run_action(run_uuid, "terminate")

    def __get_run_container_logs(
        self,
        run_uuid: str,
        pod_name: str = "",
        container_name: str = "",
    ) -> list[Logs]:
        logs_url = f"{self.users_url}/api/users/v1/runs/{run_uuid}/container_logs?pod-name={pod_name}&container-name={container_name}"

        logs_response = requests.get(
            logs_url,
            headers={"Authorization": f"Bearer {self.access_token}"},
            timeout=10,
        )

        if logs_response.status_code // 100 != 2:
            raise Exception(f"Get logs failed: {logs_response.text}")

        return [Logs.model_validate(log) for log in list(logs_response.json())]

    def __get_logs_stream(
        self,
        run_uuid: str,
        pod_name: str = "",
        container_name: str = "",
        last_event_id: str = "",
    ) -> requests.Response:
        logs_url = f"{self.users_url}/api/users/v1/runs/{run_uuid}/container_logs_stream?pod-name={pod_name}&container-name={container_name}"

        logs_response = requests.get(
            logs_url,
            stream=True,
            timeout=None,  # nosec B113
            headers={
                "Authorization": f"Bearer {self.access_token}",
                "Cache-Control": "no-cache",
                "Connection": "keep-alive",
                "last-event-id": last_event_id,
            },
        )

        if logs_response.status_code // 100 != 2:
            raise Exception(f"Get logs stream failed: {logs_response.text}")

        return logs_response

    def get_logs(
        self,
        run_uuid: str,
        pod_name: str = "",
        container_name: str = "",
    ) -> list[Logs]:
        """Get logs for a given run."""
        return self.__get_run_container_logs(run_uuid, pod_name, container_name)

    def follow_logs(
        self,
        run_uuid: str,
        pod_name: str = "",
        container_name: str = "",
    ) -> Generator[Logs, Any, None]:
        """Return a generator that yields pod logs for a given run."""
        data_msg_prefix = "data: "
        id_msg_prefix = "id: "
        ping_msg = "ping"
        close_msg = "close"
        last_event_id = ""

        while True:
            try:
                logs_stream = self.__get_logs_stream(run_uuid, pod_name, container_name, last_event_id)
                for line in logs_stream.iter_lines(delimiter="\n", decode_unicode=True):
                    line = line.strip()

                    if line == "":
                        continue

                    if line.startswith(data_msg_prefix):
                        # strip the prefix
                        line = line[len(data_msg_prefix) :]
                    elif line.startswith(id_msg_prefix):
                        last_event_id = line[len(id_msg_prefix) :]
                        continue
                    else:
                        print(f"unknown message: {line}")
                        continue

                    if line == ping_msg:
                        # pong
                        continue
                    elif line == close_msg:
                        # bye
                        return
                    else:
                        yield Logs.model_validate(json.loads(line))

            except requests.exceptions.Timeout:
                pass  # we'll ignore timeout errors and reconnect

    def __print_log_message(self, line: Logs):
        print(f"[{line.pod_name}][{line.container_name}] {line.output}")

    def print_logs(
        self,
        run_uuid: str,
        pod_name: str = "",
        container_name: str = "",
        follow: bool = True,
    ) -> None:
        """Print pod logs for a given run."""
        if follow:
            for log in self.follow_logs(run_uuid, pod_name=pod_name, container_name=container_name):
                self.__print_log_message(log)

        for log in self.get_logs(run_uuid, pod_name=pod_name, container_name=container_name):
            self.__print_log_message(log)
