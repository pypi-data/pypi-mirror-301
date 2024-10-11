import os
import sys
import argparse
import time
import traceback
from datetime import datetime

from .utils.search.actor import Search
from .session import BaseCLISession

TASK_COMPLETED = False


def log(msg):
    print("[SEARCH INDEX SESSION - %s] %s" % (
        datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S'),
        msg
    ))


def parse_remaining_args(args):
    parser = argparse.ArgumentParser(
        description='Libreflow Search Index Session Arguments'
    )
    parser.add_argument(
        '--index-uri', dest='index_uri'
    )
    parser.add_argument(
        '-p', '--project', dest='project'
    )
    values, _ = parser.parse_known_args(args)
    return (
        values.index_uri,
        values.project
    )


class SearchIndexSession(BaseCLISession):

    """
    For indexing entities coming from films and asset types
    to the Libreflow search.
    This CLI session runs once.
    """

    def __init__(self, index_uri, session_name=None, debug=False):
        self._index_uri = index_uri
        super(SearchIndexSession, self).__init__(session_name, debug)

    def _create_actors(self):
        Search(self, self._index_uri, True)
    
    def index_project(self, project_name):
        log(f'Indexing {project_name} started')
        self.cmds.Search.rebuild_project_index(project_name, f'/{project_name}/films', max_depth=7)
        self.cmds.Search.rebuild_project_index(project_name, f'/{project_name}/asset_types', max_depth=7)
        log(f'Indexing {project_name} completed')
        
        global TASK_COMPLETED
        TASK_COMPLETED = True


def main(argv):
    (
        session_name,
        host,
        port,
        cluster_name,
        db,
        password,
        debug,
        read_replica_host,
        read_replica_port,
        remaining_args,
    ) = SearchIndexSession.parse_command_line_args(argv)
    (
        index_uri,
        project_name
    ) = parse_remaining_args(remaining_args)
    session = SearchIndexSession(index_uri=index_uri,
                            session_name=session_name,
                            debug=debug,)
    session.cmds.Cluster.connect(host, port, cluster_name, db, password, read_replica_host, read_replica_port)

    while (TASK_COMPLETED is False):
        try:
            session.index_project(project_name)
            time.sleep(1)
        except (Exception, KeyboardInterrupt) as e:
            if isinstance(e, KeyboardInterrupt):
                log(f'Indexing {project_name} manually stopped')
                break
            else:
                log("The following error occurred:")
                log(traceback.format_exc())
                log("Restart indexing...")
    
    session.close()


if __name__ == "__main__":
    main(sys.argv[1:])
