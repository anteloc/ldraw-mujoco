import mujoco.viewer
from ldraw_mujoco import import_ldraw

# scene = import_ldraw("/Users/captain/tmp/ldraw-nova/output/nova-mall/mall.mpd", individual_parts=True)
scene = import_ldraw("/Users/captain/workspaces/workspace-ai/ldraw-nova/output/sakura-garden/sakura-garden.mpd", individual_parts=True)
mujoco.viewer.launch(scene.model)