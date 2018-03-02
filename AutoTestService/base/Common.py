# encoding: utf-8
import os


def get_project_path():
    """
    获取当前项目的绝对路径
    :return:
    """
    current_path = os.path.abspath(__file__)
    project_path = os.path.abspath(
        os.path.join(
            os.path.abspath(
                os.path.join(
                    os.path.abspath(os.path.join(current_path, os.pardir)),os.pardir))
            , os.pardir)
    )
    print project_path
    return project_path


def get_file_path(file_path):
    """
    根据文件的相对路径获得其绝对路径
    :param file_path:
    :return:
    """
    project = get_project_path()
    file_path = os.path.abspath(os.path.join(project, file_path))
    return file_path


def get_path_by_relative_path(file_path,config_path=None,**kwargs):
    """
    获取项目文件的绝对路径
    :param filename:
    :param config_path:
    :param kwargs:
    :return:
    """
    if config_path is not None:
        file_path=os.path.abspath(os.path.join(config_path, file_path))
    else:
        project_path = get_project_path()
        file_path = os.path.abspath(os.path.join(project_path, file_path))
    return file_path















if __name__ == "__main__":
    get_project_path()