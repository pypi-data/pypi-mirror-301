import os
import streamlit.components.v1 as components
from streamlit.components.v1.components import CustomComponent
import streamlit.elements.image as st_image
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
from hashlib import md5

IS_RELEASE = os.getenv('IS_RELEASE', 'False') == 'true'

if IS_RELEASE:
    absolute_path = os.path.dirname(os.path.abspath(__file__))
    build_path = os.path.join(absolute_path, "frontend/build")
    _component_func = components.declare_component("st-detection", path=build_path)
else:
    _component_func = components.declare_component("st-detection", url="http://localhost:3000")

def get_colormap(label_names, colormap_name='gist_rainbow'):
    colormap = {} 
    cmap = plt.get_cmap(colormap_name)
    for idx, l in enumerate(label_names):
        rgb = [int(d) for d in np.array(cmap(float(idx)/len(label_names)))*255][:3]
        colormap[l] = ('#%02x%02x%02x' % tuple(rgb))
    return colormap

#'''
#bboxes:
#[[x,y,w,h],[x,y,w,h]]
#labels:
#[0,3]
#'''
def detection(image_path, masked_image, label_list, bboxes=None, points=None, neg_points=None,labels=None, height=800, width=512, line_width=5.0, key=None, m_labels=None, is_processing=False, need_update_annotation=0, need_update_loading=0) -> CustomComponent:
    image = None
    if masked_image is not None:
        try:
            image = Image.fromarray(masked_image)
        except:
            image = masked_image
        
    else:
        image = Image.open(image_path)
    original_image_size = image.size
    image.thumbnail(size=(width, height))
    resized_image_size = image.size
    scale = original_image_size[0]/resized_image_size[0]
    
    image_url = st_image.image_to_url(image, image.size[0], True, "RGB", "PNG", f"detection-{md5(image.tobytes()).hexdigest()}-{key}")
    if image_url.startswith('/'):
        image_url = image_url[1:]
    m_labels = m_labels if m_labels else  get_colormap(label_list, colormap_name='gist_rainbow')
    bbox_info = [{'bbox':[b/scale for b in item[0]], 'label_id': item[1], 'label': item[1]} for item in zip(bboxes, labels["bboxes"]["labels"])]
    points_info = [{'point':[b/scale for b in item[0]], 'label_id': item[1], 'label': item[1]} for item in zip(points, labels["points"]["labels"])]
    neg_points_info = [{'neg_point':[b/scale for b in item[0]], 'label_id': item[1], 'label': item[1]} for item in zip(neg_points, labels["neg_points"]["labels"])]
    component_value = _component_func(image_url=image_url, image_size=image.size, label_list=label_list, bbox_info=bbox_info, points_info=points_info, neg_points_info=neg_points_info,m_labels=m_labels, line_width=line_width, is_processing=is_processing, need_update_annotation=need_update_annotation, need_update_loading=need_update_loading, key=key)
    if component_value is not None:
        component_value_bbox = {"coordinates":[[x * scale for x in bbox["coordinates"]] for bbox in component_value["bboxes"]], "labels":[bbox["label_id"] for bbox in component_value["bboxes"]]}
        component_value_point = {"coordinates": [[x * scale for x in p["coordinates"]] for p in component_value["points"]], "labels": [p["label_id"] for p in component_value["points"]]}  
        component_value_neg_point = {"coordinates": [[x * scale for x in p["coordinates"]] for p in component_value["neg_points"]], "labels": [p["label_id"] for p in component_value["neg_points"]]} 
        return {
        "bboxes": component_value_bbox,
        "points": component_value_point,
        "neg_points": component_value_neg_point
        }
    else:
        return None
        component_value_bbox = {"coordinates": [], "labels":[]}
        component_value_point = {"coordinates": [], "labels":[]}
        component_value_neg_point = {"coordinates": [], "labels":[]}
   