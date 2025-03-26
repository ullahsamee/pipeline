# This is the bash script used to generate binders to the cd20 domains focussed on hotspot residues 168 to 175
docker run -it --rm --gpus all \
   -v $HOME/models:$HOME/models \
   -v $HOME/inputs:$HOME/inputs \
   -v $HOME/outputs:$HOME/outputs \
   rfdiffusion \
   inference.output_prefix=$HOME/outputs/binder_design22 \
   inference.model_directory_path=$HOME/models \
   inference.input_pdb=$HOME/inputs/cd20.pdb \
   inference.num_designs=10 \
   'contigmap.contigs=[C46-210/0 D46-210/0 80-80]' \
   'ppi.hotspot_res=[C168,C169,C170,C171,C172,C173,C174,C175,D168,D169,D170,D171,D172,D173,D174,D175]'
