import streamlit as st
from streamlit_option_menu import option_menu
import os, sys
from streamlit.components.v1 import html as html_vis
os.chdir("c:/users/hany5/testing-app/new_superpoint_transformer")
import torch, numpy as np
from src.data import Data
from src.utils.color import to_float_rgb
from pyntcloud import PyntCloud



# Building a PLY Data reader 
file_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(file_path)

def read_ply(file_path):
    """
    Read a .ply file and return a data object with the following fields:
    - 'points': (N, 3) numpy array with the point coordinates
    - 'colors': (N, 3) numpy array with the point colors
    """
    pcd = PyntCloud.from_file(file_path)
    
    points = pcd.points
    #Extract pos data
    pos = points[['x', 'y', 'z']].values

    #Extract color data
    #colors = points[['red', 'green', 'blue']].values
    #colors = colors / 255.0


    data = Data()

    data.pos = torch.tensor(pos, dtype=torch.float32)
    #data.rgb = torch.tensor(colors, dtype=torch.float32)
    
    return data


# Building the left sidebar menu
with st.sidebar:
    selected = option_menu(
        menu_title= '⚡ SuperPoint Transformer',
        options= ['🏠 Home', '📚 How To Use', '🛠️ Segmentation Tool'],
        default_index= 0, 
    )

# Building the main content of the app
## Home page
if selected == '🏠 Home':
    
    # Apply custom CSS styles for the dark theme and improved design
    st.markdown(
        """
        <style>
        /* Set the dark mode theme for the application */
        body {
            background-color: #121212;
            color: #ffffff;
            font-family: 'Segoe UI', 'Helvetica', 'Arial', sans-serif;
        }
        /* Header styles */
        .header {
            padding: 20px;
            background-color: #1a535c;
            color: #ffffff;
            text-align: center;
            margin-bottom: 20px;
        }
        /* Logo styles */
        .logo {
            display: block;
            margin: 0 auto;
            width: 150px;
            border-radius: 50%;
        }
        /* Content styles */
        .content {

            background-color: #333;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
            margin-bottom: 20px;
        }
        /* Styles for headings and text */
        h1, h2 {
            color: #4ecdc4;
        }
        /* Button styles */
        .button {
            display: inline-block;
            padding: 10px 20px;
            background-color: #4ecdc4;
            color: #121212;
            font-size: 16px;
            font-weight: bold;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            transition: background-color 0.3s, color 0.3s;
        }
        .button:hover {
            background-color: #2b7a78;
            color: #ffffff;
        }
        /* Image styles */
        .image {
            width: 100%;
            border-radius: 10px;
            margin-top: 20px;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.5);
        }
        </style>
        """,
        unsafe_allow_html=True
    )
    st.title("Superpoint Transformer")

    st.write("The work present in this web-app is an implementation of the model presented in the paper \"Scalable 3D Panoptic Segmentation As Superpoint Graph Clustering (3DV 2024 Oral)\".")
    st.write("Make sure to visit their github and star the repo if you ❤️ the work.")
    st.link_button("SPT Github Repository","https://github.com/drprojects/superpoint_transformer")
    st.write("If you like this project, don't forget to visit my github and drop a ⭐🤩. It would be greatly appreciated! Thanks in advance!")
    st.link_button("This project's Github Repository","https://github.com/TheGitSlender/3D-Scene-Segmentator")


    st.image("./media/teaser_spt.png",output_format="auto")

    st.markdown("""**Superpoint Transformer (SPT)** is a superpoint-based transformer 🤖 architecture that efficiently ⚡ 
    performs **semantic segmentation** on large-scale 3D scenes. This method includes a 
    fast algorithm that partitions 🧩 point clouds into a hierarchical superpoint 
    structure, as well as a self-attention mechanism to exploit the relationships 
    between superpoints at multiple scales. """)
    st.markdown("""
                | ✨ SPT in numbers ✨ |
                | :---: |
                | 📊 **SOTA on S3DIS 6-Fold** (76.0 mIoU) |
                | 📊 **SOTA on KITTI-360 Val** (63.5 mIoU) |
                | 📊 **Near SOTA on DALES** (79.6 mIoU) | 
                | 🦋 **212k parameters** ([PointNeXt](https://github.com/guochengqian/PointNeXt) ÷ 200, [Stratified Transformer](https://github.com/dvlab-research/Stratified-Transformer) ÷ 40) | 
                | ⚡ S3DIS training in **3h on 1 GPU** ([PointNeXt](https://github.com/guochengqian/PointNeXt) ÷ 7, [Stratified Transformer](https://github.com/dvlab-research/Stratified-Transformer) ÷ 70) | 
                | ⚡ **Preprocessing x7 faster than [SPG](https://github.com/loicland/superpoint_graph)** |
    """)
    st.write("""This implementation of the model has been trained Areas 1-6, and tested on Area 5 of S3DIS, on a T4 GPU machine. Resulting in metrics such as: 
             Mean IoU: 69% 
             Overall Accuracy: 90%""")
    st.write("Have fun!")

# Building the guide to using the app
elif selected =="📚 How To Use":
    st.title("How to use the segmentation Tool")
    st.write("""
    1. **Upload a PLY file**: Click on the "Upload a ply file" button to upload your point cloud data in PLY format.
    2. **Segmentation Process**: Once the file is uploaded, the app will process the data and perform semantic segmentation using the Superpoint Transformer model.
    3. **Download Results**: After the segmentation is complete, you can download the HTML visualization of the segmentation results and the .pt file containing the segmentation data.
             You may preview the results on this website although it is recommended to open the HTML file in a different page.
    """)
    st.title("Navigating the visualization")
    st.write("""
        - **Right Click**: Move the user's perspective.
        - **Left Click**: Rotate the object in the 3D visualization.
        - **Scroll Up/Down**: Zoom in and out.
        """)
    st.title("Type of Visualization")
    st.write("""
    - **Position RGB**: The color defines the point's relative position to (0,0,0).
    - **Semantic Pred.**: The semantic prediction: each color represents a class, hovering the mouse on the point will show its class.
    - **Features 3D**: Each point in the point cloud can carry additional data called features. These features are numerical values (scalars or vectors) that describe certain properties of the point, such as intensity, color, or other computed attributes. This mode shows the distribution of these features across the point cloud.
    - **Level 1/2 and 3**: Represent the partition level of the superpoint architecture.
    """)
    st.write("Changing the page inside this website will not save your changes!! Make sure to download your files or preview the results of the segmentation before changing the page of your browser, or you will have to redo steps 1-3.")

# Building The segmentation tool
elif selected == '🛠️ Segmentation Tool':
     # Apply custom CSS styles for the dark theme and improved design
    st.markdown(
        """
        <style>
        /* Styles for headings and text */
        h1, h2 {
            color: #4ecdc4;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
    uploaded_file = st.file_uploader("Upload a ply file.",type=['ply'])
    import tempfile
    
    if uploaded_file is not None:
        st.write("filename:", uploaded_file.name)
        from src.data import Data
        from src.utils import init_config
        from src.transforms import instantiate_datamodule_transforms
        import hydra

        # we use init_config to load the configuration file and do the exact same preprocessing as in the training pipeline
        cfg = init_config(overrides=[f"experiment=semantic/s3dis"])

        transforms_dict = instantiate_datamodule_transforms(cfg.datamodule)

        temp_dir = tempfile.mkdtemp()
        path = os.path.join(temp_dir, uploaded_file.name)
        with open(path, "wb") as f:
            f.write(uploaded_file.getvalue())

        data = read_ply(path)
        nag = transforms_dict['pre_transform'](data)
        from src.transforms import NAGRemoveKeys

        nag = NAGRemoveKeys(level=0, keys=[k for k in nag[0].keys if k not in cfg.datamodule.point_load_keys])(nag)
        nag = NAGRemoveKeys(level='1+', keys=[k for k in nag[1].keys if k not in cfg.datamodule.segment_load_keys])(nag)

        # Move to device
        nag = nag.cuda()

        # Apply on-device transforms
        nag = transforms_dict['on_device_test_transform'](nag)


        ckpt_path = "./checkpoints/last.ckpt"
        # Instantiate the model and load pretrained weights
        model = hydra.utils.instantiate(cfg.model)
        model = model._load_from_checkpoint(ckpt_path)

        # Set the model in inference mode on the same device as the input
        model = model.eval().to(nag.device)

        # Inference, returns a task-specific ouput object carrying predictions
        with torch.no_grad():
            output = model(nag)
        # Compute the level-0 (voxel-wise) semantic segmentation predictions 
        # based on the predictions on level-1 superpoints and save those for 
        # visualization in the level-0 Data under the 'semantic_pred' attribute
        nag[0].semantic_pred = output.voxel_semantic_pred(super_index=nag[0].super_index)

        from src.datasets.s3dis import CLASS_NAMES as S3DIS_CLASS_NAMES
        from src.datasets.s3dis import CLASS_COLORS as S3DIS_CLASS_COLORS
        from src.datasets.s3dis import STUFF_CLASSES, S3DIS_NUM_CLASSES

        nag.show(
            figsize=1000,
            class_names=S3DIS_CLASS_NAMES,
            class_colors=S3DIS_CLASS_COLORS,
            stuff_classes=STUFF_CLASSES,
            num_classes=S3DIS_NUM_CLASSES,
            max_points=300000,
            title="My Interactive Visualization Partition",
            path="visualization_tests/my_interactive_visualization.html"
        )
        
        path_to_html = "visualization_tests/my_interactive_visualization.html"
        with open(path_to_html,'r') as f:
            html_data = f.read()

        # button to download the html visualization file
        st.download_button(label="Download HTML visualization",data=html_data,file_name="my_interactive_visualization.html",mime="text/html")

        # button to download the .pt nag file containing the segmentation results
        nag.save("./nag_output_files/semantic_segmentation.pt")
        st.download_button(label="Download Semantic Segmentation:",data="./nag_output_files/semantic_segmentation.pt",file_name="semantic_segmentation.pth",mime="application/octet-stream")
        
        # Visualize the results of the segmentation
        html_vis(html_data,scrolling=True,height=800,width=1200)