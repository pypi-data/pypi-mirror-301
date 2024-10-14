from __future__ import annotations # Avoid A | B annotation break under <= py3.9
import asyncio
import argparse
import os
import sys
import time
import shutil

from py2docfx import PACKAGE_ROOT
from py2docfx.convert_prepare.generate_document import generate_document
from py2docfx.convert_prepare.get_source import get_source, YAML_OUTPUT_ROOT
from py2docfx.convert_prepare.install_package import install_package
from py2docfx.convert_prepare.post_process.merge_toc import merge_toc, move_root_toc_to_target
from py2docfx.convert_prepare.params import load_file_params, load_command_params
from py2docfx.convert_prepare.package_info import PackageInfo
import py2docfx.convert_prepare.environment as py2docfxEnvironment

print("Adding yaml extension to path")
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)),'docfx_yaml'))
os.chdir(PACKAGE_ROOT)

def get_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            """A command line tool to run Sphinx with docfx-yaml extension, 
                        transform python source code packages to yamls supported in docfx"""
        )
    )

    parser.add_argument(
        "-o"
        "--output-root-folder",
        default=None,
        dest="output_root",
        help="The output folder storing generated documents, use cwd if not assigned",
    )
    parser.add_argument(
        "--github-token",
        default=None,
        dest="github_token",
        help="Allow pipeline to clone Github source code repo",
    )
    parser.add_argument(
        "--ado-token",
        default=None,
        dest="ado_token",
        help="Allow pipeline to clone Azure DevOps source code repo",
    )
    parser.add_argument(
        "-f",
        "--param-file-path",
        dest="param_file_path",
        help="The json file contains package infomation",
    )
    parser.add_argument(
        "-j",
        "--param-json",
        default=None,
        dest="param_json",
        help="The json string contains package infomation",
    )
    parser.add_argument(
        "-t",
        "--install-type",
        action="store",
        dest="install_type",
        choices=["pypi", "source_code", "dist_file"],
        help="""The type of source package, can be pip package, github repo or a distribution
                        file accessible in public""",
    )
    parser.add_argument(
        "-n",
        "--package-name",
        default=None,
        dest="package_name",
        help="The name of source package, required if INSTALL_TYPE==pypi",
    )
    parser.add_argument(
        "-v",
        "--version",
        default=None,
        dest="version",
        help="The version of source package, if not assigned, will use latest version",
    )
    parser.add_argument(
        "-i",
        "--extra-index-url",
        default=None,
        dest="extra_index_url",
        help="Extra index of pip to download source package",
    )
    parser.add_argument(
        "--url",
        default=None,
        dest="url",
        help="""Valid when INSTALL_TYPE==source_code, url of the repo to
                         clone which contains SDK package source code.""",
    )
    parser.add_argument(
        "--branch",
        default=None,
        dest="branch",
        help="""Valid when INSTALL_TYPE==source_code, branch of the repo to clone which
                         contains SDK package source code.""",
    )
    parser.add_argument(
        "--editable",
        default=False,
        dest="editable",
        help="""Install a project in editable mode.""",
    )
    parser.add_argument(
        "--folder",
        default=None,
        dest="folder",
        help="""Valid when INSTALL_TYPE==source_code, relative folder path inside the repo
                         containing SDK package source code.""",
    )
    parser.add_argument(
        "--prefer-source-distribution",
        dest="prefer_source_distribution",
        action="store_true",
        help="""Valid when INSTALL_TYPE==pypi, a flag which add --prefer-binary
                         option to pip commands when getting package source.""",
    )
    parser.add_argument(
        "--location",
        default=None,
        dest="location",
        help="""Valid when INSTALL_TYPE==dist_file, the url of distribution file
                         containing source package.""",
    )
    parser.add_argument(
        "--build-in-subpackage",
        action="store_true",
        dest="build_in_subpackage",
        help="""When package has lot of big subpackages and each doesn't depend on others
                    enable to fasten build""",
    )
    parser.add_argument(
        "exclude_path",
        default=[],
        nargs="*",
        help="""A list containing relative paths to the root of the package of files/directories
                         excluded when generating documents, should follow fnmatch-style.""",
    )
    return parser


def parse_command_line_args(argv) -> (
        list[PackageInfo], list[PackageInfo], str, str, str | os.PathLike, bool):
    parser = get_parser()
    args = parser.parse_args(argv)

    github_token = args.github_token
    ado_token = args.ado_token
    output_root = args.output_root

    if args.param_file_path:
        (package_info_list, required_packages) = load_file_params(args.param_file_path)
        return (list(package_info_list), list(required_packages), github_token,
                ado_token, output_root)
    elif args.param_json:
        (package_info_list, required_packages) = load_command_params(args.param_json)
        return (package_info_list, required_packages, github_token,
                ado_token, output_root)
    else:
        package_info = PackageInfo()
        if not args.install_type:
            PackageInfo.report_error("install_type", args.install_type)
        package_info.install_type = PackageInfo.InstallType[
            args.install_type.upper()
        ]

        package_info.name = args.package_name
        package_info.version = args.version
        package_info.extra_index_url = args.extra_index_url
        package_info.editable = args.editable
        package_info.prefer_source_distribution = (
            args.prefer_source_distribution
        )
        package_info.build_in_subpackage = args.build_in_subpackage
        package_info.exclude_path = args.exclude_path

        if (
            package_info.install_type == PackageInfo.InstallType.PYPI
            and not package_info.name
        ):
            PackageInfo.report_error("name", "None")

        if package_info.install_type == PackageInfo.InstallType.SOURCE_CODE:
            package_info.url = args.url
            package_info.branch = args.branch
            package_info.folder = args.folder
            if not package_info.url:
                if not package_info.folder:
                    raise ValueError(
                        "When install_type is source_code, folder or url should be provided"
                    )
                else:
                    print(f'Read source code from local folder: {package_info.folder}')

        if package_info.install_type == PackageInfo.InstallType.DIST_FILE:
            package_info.location = args.location
            if not package_info.location:
                PackageInfo.report_error(
                    "location",
                    "None",
                    condition="When install_type is dist_file",
                )
        return ([package_info], [], github_token, ado_token, output_root)

import py2docfx.convert_prepare.pip_utils as pip_utils


# async def create_venv_async(venv_dir: os.PathLike, package: PackageInfo) -> None:
#     subprocess.run([sys.executable, "-m", "venv", venv_dir], check=True)
#     venv_exe = os.path.join(venv_dir, "Scripts", "python.exe")
#     subprocess.run([venv_exe, "-m", "pip", "install", "sphinx==6.1.3"], check=True)
#     subprocess.run([venv_exe, "-m", "pip", "install", "setuptools"], check=True)
#     subprocess.run([venv_exe, "-m", "pip", "install", "pyyaml"], check=True)
#     subprocess.run([venv_exe, "-m", "pip", "install", "jinja2==3.0.3"], check=True)
#     if package.version:
#         pkg_install_str = package.name + "==" + package.version
#     else:
#         pkg_install_str = package.name
#     subprocess.run([venv_exe, "-m", "pip", "install", pkg_install_str], check=True)
#     return venv_exe

from py2docfx.convert_prepare.environment import install_converter_requirements

async def donwload_package_generate_documents(
        package_info_list: list[PackageInfo],
        output_root: str | os.PathLike | None,
        output_doc_folder: os.PathLike | None,
        github_token: str, ado_token: str, required_package_list: list):
    
    start_num = len(required_package_list)
    env_prepare_tasks = []
    env_remove_tasks = []

    start_time = time.time()
    for idx in range(min([py2docfxEnvironment.VENV_BUFFER, len(package_info_list)])):
        package_info = package_info_list[idx]
        package_number = start_num + idx
        env_prepare_tasks.append(
            asyncio.create_task(py2docfxEnvironment.prepare_venv(idx, package_info, package_number, github_token, ado_token)))
    await asyncio.create_task(
            py2docfxEnvironment.prepare_base_venv(required_package_list, github_token, ado_token))
    end_time = time.time()
    print(f"<warmup_venvs>{end_time-start_time}<warmup_venvs/>")

    for idx, package in enumerate(package_info_list):
        package_number = start_num + idx
        print(f"Processing package {package.name}, env_prepare_tasks: {len(env_prepare_tasks)}")
        start_time = time.time()
        try:
            await env_prepare_tasks[idx]
        except Exception as e:
            print(f"Failed to setup venv for package {package.name}: {e}")
            raise
        end_time = time.time()
        print(f"<wait_prepare_venv>{package.name},{end_time-start_time}<wait_prepare_venv/>")

        # start_time = time.time()
        # get_source(py2docfxEnvironment.get_venv_exe(idx), package, package_number, vststoken=ado_token, githubtoken=github_token)
        # end_time = time.time()
        # print(f"<get_source>{package.name},{end_time-start_time}<get_source/>")

        # start_time = time.time()
        # package_name, options = package.get_install_command()
        # try:
        #     pip_utils.install_in_exe(py2docfxEnvironment.get_venv_exe(idx), package_name, options)
        # except Exception as e:
        #     print(f"Install package failed: {e}")
        #     raise

        # end_time = time.time()
        # print(f"<install_package>{package.name},{end_time-start_time}<install_package/>")

        # venv_dir = os.path.join(PACKAGE_ROOT, "venv", "0")
        # venv_exe = asyncio.run(create_venv_async(venv_dir, package))

        start_time = time.time()
        generate_document(package, output_root,
                          py2docfxEnvironment.get_base_venv_sphinx_build_path(),
                          py2docfxEnvironment.get_venv_package_path(idx), 
                          py2docfxEnvironment.get_base_venv_exe())
        end_time = time.time()
        print(f"<generate_document>{package.name},{end_time-start_time}<generate_document/>")

        start_time = time.time()
        merge_toc(YAML_OUTPUT_ROOT, package.path.yaml_output_folder)
        end_time = time.time()
        print(f"<merge_toc>{package.name},{end_time-start_time}<merge_toc/>")

        if output_doc_folder:
            start_time = time.time()
            package.path.move_document_to_target(os.path.join(output_doc_folder, package.name))
            end_time = time.time()
            print(f"<move_document_to_target>{package.name},{end_time-start_time}<move_document_to_target/>")
        
        start_time = time.time()
        if idx + py2docfxEnvironment.VENV_BUFFER < len(package_info_list):
            buffer_package_idx = idx + py2docfxEnvironment.VENV_BUFFER
            print(f"Creating venv {buffer_package_idx}")
            env_prepare_tasks.append(
                asyncio.create_task(py2docfxEnvironment.prepare_venv(buffer_package_idx, 
                                                                     package_info_list[buffer_package_idx], 
                                                                     start_num + buffer_package_idx, 
                                                                     github_token, 
                                                                     ado_token)))
        end_time = time.time()
        print(f"<create_prepare_venv>{package.name},{end_time-start_time}<create_prepare_venv/>")
        if idx >= 1:
            start_time = time.time()
            env_remove_tasks.append(asyncio.create_task(
                py2docfxEnvironment.remove_environment(idx-1)))
            end_time = time.time()
            print(f"<create_remove_venv>{package.name},{end_time-start_time}<create_remove_venv/>")
        if idx > py2docfxEnvironment.VENV_BUFFER and env_remove_tasks[idx-py2docfxEnvironment.VENV_BUFFER] != None:
            start_time = time.time()
            print(f"Removing venv {idx-py2docfxEnvironment.VENV_BUFFER}")
            await env_remove_tasks[idx-py2docfxEnvironment.VENV_BUFFER]
            end_time = time.time()
            print(f"<wait_remove_venv>{package.name},{end_time-start_time}<wait_remove_venv/>")
    
    if output_doc_folder:
        start_time = time.time()
        move_root_toc_to_target(YAML_OUTPUT_ROOT, output_doc_folder)
        end_time = time.time()
        print(f"<move_root_toc_to_target>{end_time-start_time}<move_root_toc_to_target/>")
    
    start_time = time.time()
    for idx in range(len(env_remove_tasks)):
        if env_remove_tasks[idx] != None and not env_remove_tasks[idx].done():
            await env_remove_tasks[idx]
    end_time = time.time()
    print(f"<wait_remove_venv>{end_time-start_time}<wait_remove_venv/>")

def prepare_out_dir(output_root: str | os.PathLike) -> os.PathLike | None:
    # prepare output_root\DOC_FOLDER_NAME (if folder contains files, raise exception)
    if output_root:
        if os.path.exists(output_root):
            if os.path.isfile(output_root):
                raise ValueError(f"""output-root-folder is a path of file,
                                 output-root-folder value: {output_root}""")
            else:
                if len(os.listdir(output_root)) > 0:
                    raise ValueError(f"""output-root-folder isn't empty,
                                    output-root-folder value: {output_root}""")
                return output_root
        else:
            os.makedirs(output_root)
            return output_root
    else:
        return None

def temp_folder_clean_up(folder_list: list[str | os.PathLike]) -> None:
    for folder in folder_list:
        if os.path.exists(folder):
            shutil.rmtree(folder)

def main(argv) -> int:
    # clean up TODO: limit those folders to only use py2docfx install position and use a method to iterate
    clean_up_folder_list = [py2docfxEnvironment.VENV_DIR, "dist_temp", "source_repo", "target_repo"]
    temp_folder_clean_up(clean_up_folder_list)

    # TODO: may need to purge pip cache
    (package_info_list,
     required_package_list,
     github_token, ado_token,
     output_root) = parse_command_line_args(argv)
    
    output_doc_folder = prepare_out_dir(output_root)

    # start_time = time.time()
    # install_required_packages(required_package_list, github_token, ado_token)
    # end_time = time.time()
    # print(f"<install_required_packages>{end_time-start_time}<install_required_packages/>")

    start_time = time.time()
    try:
        asyncio.run(donwload_package_generate_documents(
            package_info_list, output_root, output_doc_folder,
            github_token, ado_token, required_package_list))
    except Exception as e:
        print(f"An error occurred: {e}")
        raise
    end_time = time.time()
    print(f"<donwload_package_generate_documents>{end_time-start_time}<donwload_package_generate_documents/>")
    return 0

if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
