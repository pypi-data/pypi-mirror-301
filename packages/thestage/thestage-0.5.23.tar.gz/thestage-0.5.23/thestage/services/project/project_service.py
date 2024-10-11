from typing import Optional

import click
import typer
from git import Commit
from tabulate import tabulate
from thestage_core.entities.config_entity import ConfigEntity
from thestage_core.exceptions.http_error_exception import HttpClientException
from thestage_core.services.filesystem_service import FileSystemServiceCore

from thestage.color_scheme.color_scheme import ColorScheme
from thestage.entities.enums.yes_no_response import YesOrNoResponse
from thestage.exceptions.git_access_exception import GitAccessException
from thestage.i18n.translation import __
from thestage.services.clients.git.git_client import GitLocalClient
from thestage.services.clients.thestage_api.dtos.container_response import DockerContainerDto
from thestage.services.clients.thestage_api.dtos.enums.container_status import DockerContainerStatus
from thestage.services.clients.thestage_api.dtos.paginated_entity_list import PaginatedEntityList
from thestage.services.clients.thestage_api.dtos.project_controller.project_run_task_response import \
    ProjectRunTaskResponse
from thestage.services.clients.thestage_api.dtos.project_response import ProjectDto
from thestage.services.clients.thestage_api.dtos.task_controller.task_view_response import TaskViewResponse
from thestage.services.task.dto.task_dto import TaskDto
from thestage.services.project.dto.project_config import ProjectConfig
from thestage.services.project.mapper.project_task_mapper import ProjectTaskMapper
from thestage.services.remote_server_service import RemoteServerService
from thestage.services.abstract_service import AbstractService
from thestage.helpers.error_handler import error_handler
from thestage.services.clients.thestage_api.api_client import TheStageApiClient
from thestage.services.config_provider.config_provider import ConfigProvider
from rich import print


class ProjectService(AbstractService):
    __thestage_api_client: TheStageApiClient = None

    def __init__(
            self,
            thestage_api_client: TheStageApiClient,
            config_provider: ConfigProvider,
            remote_server_service: RemoteServerService,
            file_system_service: FileSystemServiceCore,
            git_local_client: GitLocalClient,
    ):
        super(ProjectService, self).__init__(
            config_provider=config_provider
        )
        self.__thestage_api_client = thestage_api_client
        self.__remote_server_service = remote_server_service
        self.__file_system_service = file_system_service
        self.__git_local_client = git_local_client
        self.__project_task_mapper = ProjectTaskMapper()
        self.__config_provider = config_provider

    @error_handler()
    def get_project_by_slug_and_check_if_present(
            self,
            config: ConfigEntity,
            project_slug: Optional[str] = None,
    ) -> Optional[ProjectDto]:
        if not project_slug:
            typer.echo(__('Please go to site and create new project or select present'))
            project_slug: str = typer.prompt(
                text=__('Please give me sketch slug'),
                show_choices=False,
                type=str,
                show_default=False,
            )
            if not project_slug:
                typer.echo(__('Slug can not be empty'))
                raise typer.Exit(1)

        project: Optional[ProjectDto] = self.__thestage_api_client.get_project_by_slug(
            slug=project_slug,
            token=config.main.thestage_auth_token,
        )

        if not project:
            typer.echo(__('You entered the wrong slug, sketch not found'))
            raise typer.Exit(1)

        return project

    @error_handler()
    def init_project(
            self,
            config: ConfigEntity,
            project_slug: str,
    ):
        project = self.get_project_by_slug_and_check_if_present(
            config=config,
            project_slug=project_slug,
        )

        is_git_folder = self.__git_local_client.is_present_local_git(
            path=config.runtime.working_directory,
        )
        if is_git_folder:
            has_remote = self.__git_local_client.has_remote(
                path=config.runtime.working_directory,
            )
            if has_remote:
                typer.echo(__('You have local repo with remote, we can not work with this'))
                raise typer.Exit(1)

        if not project.git_repository_url:
            typer.echo(__('Sketch dont have git repository url'))
            raise typer.Exit(1)

        if project.last_commit_hash or project.last_commit_description:
            continue_with_non_empty_repo: YesOrNoResponse = typer.prompt(
                text=__('Remote repository is probably not empty: latest commit is "{commit_description}" (sha: {commit_hash})\nDo you wish to continue?').format(commit_description=project.last_commit_description, commit_hash=project.last_commit_hash),
                show_choices=True,
                default=YesOrNoResponse.YES.value,
                type=click.Choice([r.value for r in YesOrNoResponse]),
                show_default=True,
            )
            if continue_with_non_empty_repo == YesOrNoResponse.NO:
                typer.echo(__('Project init aborted'))
                raise typer.Exit(0)

        deploy_ssh_key = self.__thestage_api_client.get_project_deploy_ssh_key(
            slug=project.slug,
            token=config.main.thestage_auth_token
        )

        deploy_key_path = self.__config_provider.save_project_deploy_ssh_key(
            deploy_ssh_key=deploy_ssh_key,
            slug=project.slug
        )

        if is_git_folder:
            has_changes = self.__git_local_client.has_changes_with_untracked(
                path=config.runtime.working_directory,
            )
            if has_changes:
                typer.echo(__('You local repo has changes and not empty, please create empty folder'))
                raise typer.Exit(1)
        else:
            repo = self.__git_local_client.init_repository(
                path=config.runtime.working_directory,
            )

        is_remote_added = self.__git_local_client.add_remote_to_repo(
            path=config.runtime.working_directory,
            remote_url=project.git_repository_url,
            remote_name=project.git_repository_name,
        )
        if not is_remote_added:
            typer.echo(__('We can not add remote, something wrong'))
            raise typer.Exit(2)

        self.__git_local_client.git_fetch(path=config.runtime.working_directory, deploy_key_path=deploy_key_path)

        branch = self.__git_local_client.find_main_branch_name(path=config.runtime.working_directory, )
        if branch:
            self.__git_local_client.git_pull(path=config.runtime.working_directory, deploy_key_path=deploy_key_path,
                                             branch=branch)

        self.__git_local_client.init_gitignore(path=config.runtime.working_directory)

        self.__git_local_client.git_add_all(repo_path=config.runtime.working_directory)

        project_config = ProjectConfig()
        project_config.id = project.id
        project_config.slug = project.slug
        project_config.git_repository_url = project.git_repository_url
        project_config.deploy_key_path = str(deploy_key_path)
        self.__config_provider.save_project_config(project_config=project_config)


    @error_handler()
    def clone_project(
            self,
            config: ConfigEntity,
            project_slug: str,
    ):
        if not self.__file_system_service.is_folder_empty(folder=config.runtime.working_directory, auto_create=True):
            typer.echo(__("Cannot clone: the folder is not empty"))
            raise typer.Exit(1)

        project = self.get_project_by_slug_and_check_if_present(
            config=config,
            project_slug=project_slug,
        )

        is_git_folder = self.__git_local_client.is_present_local_git(
            path=config.runtime.working_directory,
        )

        if is_git_folder:
            typer.echo(__('You have local repo, we can not work with this'))
            raise typer.Exit(1)

        if not project.git_repository_url:
            typer.echo(__("Unexpected Project error, missing Repository"))
            raise typer.Exit(1)

        deploy_ssh_key = self.__thestage_api_client.get_project_deploy_ssh_key(slug=project.slug, token=config.main.thestage_auth_token)
        deploy_key_path = self.__config_provider.save_project_deploy_ssh_key(deploy_ssh_key=deploy_ssh_key, slug=project.slug)

        try:
            self.__git_local_client.clone(
                url=project.git_repository_url,
                path=config.runtime.working_directory,
                deploy_key_path=deploy_key_path
            )
            self.__git_local_client.init_gitignore(path=config.runtime.working_directory)
        except GitAccessException as ex:
            typer.echo(ex.get_message())
            typer.echo(ex.get_dop_message())
            typer.echo(__(
                "Please check you mail or open this repo url %git_url% and 'Accept invitation'",
                {
                    'git_url': ex.get_url()
                }
            ))
            raise typer.Exit(1)

        project_config = ProjectConfig()
        project_config.id = project.id
        project_config.slug = project.slug
        project_config.git_repository_url = project.git_repository_url
        project_config.deploy_key_path = str(deploy_key_path)
        self.__config_provider.save_project_config(project_config=project_config)


    @error_handler()
    def project_run_task(
            self,
            config: ConfigEntity,
            run_command: str,
            task_title: Optional[str] = None,
            commit_hash: Optional[str] = None,
            docker_container_slug: Optional[str] = None,
    ) -> Optional[TaskDto]:
        project_config: ProjectConfig = self.__config_provider.read_project_config()
        if not project_config:
            typer.echo(__("No project found at the path: %path%. Please initialize or clone a project first.", {"path": config.runtime.working_directory}))
            raise typer.Exit(1)

        if not docker_container_slug and not project_config.default_container_uid:
            typer.echo(__('Docker container unique ID is required'))
            raise typer.Exit(1)

        container_slug_for_task = docker_container_slug if docker_container_slug else project_config.default_container_uid

        if not docker_container_slug:
            typer.echo(f"Using default docker container for this project: '{container_slug_for_task}'")

        container: DockerContainerDto = self.__thestage_api_client.get_container(
            token=config.main.thestage_auth_token,
            container_slug=container_slug_for_task,
        )

        if container is None:
            typer.echo(f"Could not find container '{container_slug_for_task}'")
            if project_config.default_container_uid == container_slug_for_task:
                project_config.default_container_uid = None
                project_config.prompt_for_default_container = True
                self.__config_provider.save_project_config(project_config=project_config)
                typer.echo(f"Default container settings were reset")
            raise typer.Exit(1)

        if container.project_id != project_config.id:
            typer.echo(f"Provided container '{docker_container_slug}' is not related to project '{project_config.slug}'")
            raise typer.Exit(1)

        if (project_config.prompt_for_default_container is None or project_config.prompt_for_default_container) and docker_container_slug and (project_config.default_container_uid != docker_container_slug):
            set_default_container_slug: str = typer.prompt(
                text=f"Would you like to set '{docker_container_slug}' as a default container for this project installation?",
                show_choices=True,
                default=YesOrNoResponse.YES.value,
                type=click.Choice([r.value for r in YesOrNoResponse]),
                show_default=True,
            )
            project_config.prompt_for_default_container = False
            if set_default_container_slug == YesOrNoResponse.YES.value:
                project_config.default_container_uid = docker_container_slug

            self.__config_provider.save_project_config(project_config=project_config)

        if not commit_hash:
            is_git_folder = self.__git_local_client.is_present_local_git(path=config.runtime.working_directory)
            if not is_git_folder:
                typer.echo("Error: working directory does not contain git repository")
                raise typer.Exit(1)

            is_commit_allowed: bool = True
            has_changes = self.__git_local_client.has_changes_with_untracked(
                path=config.runtime.working_directory,
            )

            if self.__git_local_client.is_head_detached(path=config.runtime.working_directory):
                print(f"[{ColorScheme.GIT_HEADLESS.value}]HEAD is detached[{ColorScheme.GIT_HEADLESS.value}]")

                is_headless_commits_present = self.__git_local_client.is_head_committed_in_headless_state(path=config.runtime.working_directory)
                if is_headless_commits_present:
                    print(f"[{ColorScheme.GIT_HEADLESS.value}]Current commit was made in detached head state. Cannot use it to run the task. Consider using 'project checkout' command to return to a valid reference.[{ColorScheme.GIT_HEADLESS.value}]")
                    raise typer.Exit(1)

                if has_changes:
                    print(f"[{ColorScheme.GIT_HEADLESS.value}]Local changes detected in detached head state. They will not impact the task execution.[{ColorScheme.GIT_HEADLESS.value}]")
                    is_commit_allowed = False
                    response: YesOrNoResponse = typer.prompt(
                        text=__('Continue?'),
                        show_choices=True,
                        default=YesOrNoResponse.YES.value,
                        type=click.Choice([r.value for r in YesOrNoResponse]),
                        show_default=True,
                    )
                    if response == YesOrNoResponse.NO:
                        raise typer.Exit(0)

            if is_commit_allowed:
                self.__git_local_client.git_add_all(repo_path=config.runtime.working_directory)

                if has_changes:
                    branch_name = self.__git_local_client.get_active_branch_name(config.runtime.working_directory)
                    diff_stat = self.__git_local_client.git_diff_stat(repo_path=config.runtime.working_directory)
                    typer.echo(__('Active branch [%branch_name%] has uncommitted changes: %diff_stat_bottomline%', {
                        'diff_stat_bottomline': diff_stat,
                        'branch_name': branch_name,
                    }))

                    response: str = typer.prompt(
                        text=__('Commit changes?'),
                        show_choices=True,
                        default=YesOrNoResponse.YES.value,
                        type=click.Choice([r.value for r in YesOrNoResponse]),
                        show_default=True,
                    )
                    if response == YesOrNoResponse.NO.value:
                        typer.echo("Task cannot use uncommitted changes - aborting")
                        raise typer.Exit(0)

                    commit_name = typer.prompt(
                        text=__('Please provide commit message'),
                        show_choices=False,
                        type=str,
                        show_default=False,
                    )

                    if commit_name:
                        commit_result = self.__git_local_client.commit_local_changes(
                            path=config.runtime.working_directory,
                            name=commit_name
                        )

                        if commit_result:
                            # in docs not Commit object, on real - str
                            if isinstance(commit_result, str):
                                typer.echo(commit_result)

                        self.__git_local_client.push_changes(
                            path=config.runtime.working_directory,
                            deploy_key_path=project_config.deploy_key_path
                        )
                        typer.echo(__("Pushed changes to remote repository"))
                    else:
                        typer.echo(__('Cannot commit with empty commit name, your code will run without last changes.'))
                else:
                    pass
                    # possible to push new empty branch - only that there's a wrong place to do so
            commit = self.__git_local_client.get_current_commit(path=config.runtime.working_directory)
            if commit and isinstance(commit, Commit):
                commit_hash = commit.hexsha

        if not task_title:
            typer.echo(__("Please provide task title"))

            auto_title = "Task for project {slug}".format(slug=project_config.slug)
            title: str = typer.prompt(
                text=__('New task title:'),
                show_choices=False,
                default=auto_title,
                type=str,
                show_default=True,
            )
            if not title:
                typer.echo(__("Task title can not be empty"))
                raise typer.Exit(1)
            else:
                task_title = title

        run_task_response: ProjectRunTaskResponse = self.__thestage_api_client.execute_project_task(
            token=config.main.thestage_auth_token,
            project_slug=project_config.slug,
            docker_container_slug=container_slug_for_task,
            run_command=run_command,
            commit_hash=commit_hash,
            task_title=task_title,
        )
        if run_task_response:
            if run_task_response.message:
                typer.echo(run_task_response.message)
            if run_task_response.is_success and run_task_response.task:
                typer.echo(__("Task has been scheduled successfully. Task ID: %task_id%", {'task_id': str(run_task_response.task.id)}))
                return run_task_response.task
            else:
                typer.echo(__(
                    'The task failed with an error: %server_massage%',
                    {'server_massage': run_task_response.message or ""}
                ))
                raise typer.Exit(1)
        else:
            typer.echo(__("The task failed with an error"))
            raise typer.Exit(1)


    @error_handler()
    def get_project_task_list(
            self,
            config: ConfigEntity,
            project_slug: str,
            row: int = 5,
            page: int = 1,
    ) -> PaginatedEntityList[TaskDto]:
        data: Optional[PaginatedEntityList[TaskDto]] = self.__thestage_api_client.get_task_list_for_project(
            token=config.main.thestage_auth_token,
            project_slug=project_slug,
            page=page,
            limit=row,
        )

        return data


    @error_handler()
    def checkout_project(
            self,
            config: ConfigEntity,
            task_id: Optional[int],
            branch_name: Optional[str],
    ):
        project_config: ProjectConfig = self.__config_provider.read_project_config()
        if not project_config:
            typer.echo(__("This command is only allowed from within an initialized project directory"))
            raise typer.Exit(1)

        target_commit_hash: Optional[str] = None
        if task_id:
            task_view_response: Optional[TaskViewResponse] = None
            try:
                task_view_response = self.__thestage_api_client.get_task(
                    token=config.main.thestage_auth_token,
                    task_id=task_id,
                )
            except HttpClientException as e:
                if e.get_status_code() == 400:
                    typer.echo(f"Task {task_id} was not found")
                    # overriding arguments here
                    branch_name = str(task_id)
                    task_id = None

            if task_view_response and task_view_response.task:
                target_commit_hash = task_view_response.task.commit_hash
                if not target_commit_hash:
                    typer.echo(f"Provided task ({task_id}) has no commit hash")  # possible legacy problems
                    raise typer.Exit(1)

        is_commit_allowed: bool = True

        if self.__git_local_client.is_head_detached(path=config.runtime.working_directory):
            is_commit_allowed = False
            if self.__git_local_client.is_head_committed_in_headless_state(path=config.runtime.working_directory):
                commit_message = self.__git_local_client.get_current_commit(path=config.runtime.working_directory).message
                print(f"[{ColorScheme.GIT_HEADLESS.value}]Your current commit '{commit_message.strip()}' was likely created in detached head state. Checking out will discard all changes.[/{ColorScheme.GIT_HEADLESS.value}]")
                response: YesOrNoResponse = typer.prompt(
                    text=__('Continue?'),
                    show_choices=True,
                    default=YesOrNoResponse.YES.value,
                    type=click.Choice([r.value for r in YesOrNoResponse]),
                    show_default=True,
                )
                if response == YesOrNoResponse.NO:
                    raise typer.Exit(0)
        else:
            if self.__git_local_client.get_active_branch_name(path=config.runtime.working_directory) == branch_name:
                typer.echo(f"You are already at branch '{branch_name}'")
                raise typer.Exit(0)

        if is_commit_allowed:
            self.__git_local_client.git_add_all(repo_path=config.runtime.working_directory)

            has_changes = self.__git_local_client.has_changes_with_untracked(
                path=config.runtime.working_directory,
            )
            if has_changes:
                active_branch_name = self.__git_local_client.get_active_branch_name(config.runtime.working_directory)
                diff_stat = self.__git_local_client.git_diff_stat(repo_path=config.runtime.working_directory)
                typer.echo(__('Active branch [%branch_name%] has uncommitted changes: %diff_stat_bottomline%', {
                    'diff_stat_bottomline': diff_stat,
                    'branch_name': active_branch_name,
                }))

                response: str = typer.prompt(
                    text=__('Commit changes?'),
                    show_choices=True,
                    default=YesOrNoResponse.YES.value,
                    type=click.Choice([r.value for r in YesOrNoResponse]),
                    show_default=True,
                )
                if response == YesOrNoResponse.NO.value:
                    typer.echo(__('Cannot checkout with uncommitted changes'))
                    raise typer.Exit(0)

                commit_name = typer.prompt(
                    text=__('Please provide commit message'),
                    show_choices=False,
                    type=str,
                    show_default=False,
                )

                if commit_name:
                    commit_result = self.__git_local_client.commit_local_changes(
                        path=config.runtime.working_directory,
                        name=commit_name
                    )

                    if commit_result:
                        # in docs not Commit object, on real - str
                        if isinstance(commit_result, str):
                            typer.echo(commit_result)

                    self.__git_local_client.push_changes(
                        path=config.runtime.working_directory,
                        deploy_key_path=project_config.deploy_key_path
                    )
                    typer.echo(__("Pushed changes to remote repository"))
                else:
                    typer.echo(__('Cannot commit with empty commit name'))
                    raise typer.Exit(0)

        if target_commit_hash:
            if self.__git_local_client.get_current_commit(path=config.runtime.working_directory).hexsha != target_commit_hash:
                is_checkout_successful = self.__git_local_client.git_checkout_to_commit(
                    path=config.runtime.working_directory,
                    commit_hash=target_commit_hash
                )

                if is_checkout_successful:
                    print(f"Checked out to commit {target_commit_hash}")
                    print(f"[{ColorScheme.GIT_HEADLESS.value}]HEAD is detached. To be able make changes in repository, checkout to any branch.[/{ColorScheme.GIT_HEADLESS.value}]")
            else:
                typer.echo("HEAD is already at requested commit")
        elif branch_name:
            if self.__git_local_client.is_branch_exists(path=config.runtime.working_directory, branch_name=branch_name):
                self.__git_local_client.git_checkout_to_branch(
                    path=config.runtime.working_directory,
                    branch=branch_name
                )
                typer.echo(f"Checked out to branch '{branch_name}'")
            else:
                typer.echo(f"Branch '{branch_name}' was not found in project repository")
        else:
            main_branch = self.__git_local_client.find_main_branch_name(path=config.runtime.working_directory)
            if main_branch:
                self.__git_local_client.git_checkout_to_branch(
                    path=config.runtime.working_directory,
                    branch=main_branch
                )
                typer.echo(f"Checked out to detected main branch: '{main_branch}'")
            else:
                typer.echo("No main branch found")


    @error_handler()
    def set_default_container(self, config: ConfigEntity, container_uid: Optional[str]):
        project_config: ProjectConfig = self.__config_provider.read_project_config()

        if project_config is None:
            typer.echo(f"No project found in working directory")
            raise typer.Exit(1)

        if container_uid:
            container: DockerContainerDto = self.__thestage_api_client.get_container(
                token=config.main.thestage_auth_token,
                container_slug=container_uid,
            )
            if container is None:
                typer.echo(f"Could not find container '{container_uid}'")
                raise typer.Exit(1)

            if container.project_id != project_config.id:
                typer.echo(f"Provided container '{container_uid}' is not related to project '{project_config.slug}'")
                raise typer.Exit(1)

            if container.frontend_status.status_key != DockerContainerStatus.RUNNING:
                typer.echo(f"Note: provided container '{container_uid}' is in status '{container.frontend_status.status_translation}'")

        project_config.default_container_uid = container_uid
        project_config.prompt_for_default_container = False
        self.__config_provider.save_project_config(project_config=project_config)
        typer.echo("Default container settings were updated")


    @error_handler()
    def unset_default_container(self):
        project_config: ProjectConfig = self.__config_provider.read_project_config()

        if project_config is None:
            typer.echo(f"No project found in working directory")
            raise typer.Exit(1)

        project_config.default_container_uid = None
        project_config.prompt_for_default_container = True  # True or False?
        self.__config_provider.save_project_config(project_config=project_config)
        typer.echo("Default container settings were updated")


    @error_handler()
    def print_project_config(self, config):
        project_config: ProjectConfig = self.__config_provider.read_project_config()

        if project_config is None:
            typer.echo(f"No project found in working directory")
            raise typer.Exit(1)

        typer.echo(tabulate(
            [
                [
                    "Project unique ID", project_config.slug
                ],
                [
                    "Default docker container unique ID", project_config.default_container_uid if project_config.default_container_uid else "<None>"
                ],
            ],
            showindex=False,
            tablefmt="simple",
        ))
