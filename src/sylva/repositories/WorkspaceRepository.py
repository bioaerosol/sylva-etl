import typing
import os
import uuid

class WorkspaceRepository:
    
    def create_workspace(self, workspace_base_path: str, workspace_id: str, absolute_files_names: typing.List[str]) -> str:        
        workspace_path = os.path.join(workspace_base_path, workspace_id)
        os.makedirs(workspace_path)

        for file in absolute_files_names:
            os.link(file, os.path.join(workspace_path, str(uuid.uuid4())[:8] + "_" + os.path.basename(file)))

        return workspace_path