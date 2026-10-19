mkdir ./checkpoints  

# lagency download link
# curl -L --create-dirs https://github.com/Winfredy/SadTalker/releases/download/v0.0.2/auido2exp_00300-model.pth -o ./checkpoints/auido2exp_00300-model.pth
# curl -L --create-dirs https://github.com/Winfredy/SadTalker/releases/download/v0.0.2/auido2pose_00140-model.pth -o ./checkpoints/auido2pose_00140-model.pth
# curl -L --create-dirs https://github.com/Winfredy/SadTalker/releases/download/v0.0.2/epoch_20.pth -o ./checkpoints/epoch_20.pth
# curl -L --create-dirs https://github.com/Winfredy/SadTalker/releases/download/v0.0.2/facevid2vid_00189-model.pth.tar -o ./checkpoints/facevid2vid_00189-model.pth.tar
# curl -L --create-dirs https://github.com/Winfredy/SadTalker/releases/download/v0.0.2/shape_predictor_68_face_landmarks.dat -o ./checkpoints/shape_predictor_68_face_landmarks.dat
# curl -L --create-dirs https://github.com/Winfredy/SadTalker/releases/download/v0.0.2/wav2lip.pth -o ./checkpoints/wav2lip.pth
# curl -L --create-dirs https://github.com/Winfredy/SadTalker/releases/download/v0.0.2/mapping_00229-model.pth.tar -o ./checkpoints/mapping_00229-model.pth.tar
# curl -L --create-dirs https://github.com/Winfredy/SadTalker/releases/download/v0.0.2/mapping_00109-model.pth.tar -o ./checkpoints/mapping_00109-model.pth.tar
# curl -L --create-dirs https://github.com/Winfredy/SadTalker/releases/download/v0.0.2/hub.zip -o ./checkpoints/hub.zip
# unzip -n ./checkpoints/hub.zip -d ./checkpoints/


#### download the new links.
curl -L --create-dirs https://github.com/OpenTalker/SadTalker/releases/download/v0.0.2-rc/mapping_00109-model.pth.tar -o ./checkpoints/mapping_00109-model.pth.tar
curl -L --create-dirs https://github.com/OpenTalker/SadTalker/releases/download/v0.0.2-rc/mapping_00229-model.pth.tar -o ./checkpoints/mapping_00229-model.pth.tar
curl -L --create-dirs https://github.com/OpenTalker/SadTalker/releases/download/v0.0.2-rc/SadTalker_V0.0.2_256.safetensors -o ./checkpoints/SadTalker_V0.0.2_256.safetensors
curl -L --create-dirs https://github.com/OpenTalker/SadTalker/releases/download/v0.0.2-rc/SadTalker_V0.0.2_512.safetensors -o ./checkpoints/SadTalker_V0.0.2_512.safetensors


# curl -L --create-dirs https://github.com/Winfredy/SadTalker/releases/download/v0.0.2/BFM_Fitting.zip -o ./checkpoints/BFM_Fitting.zip
# unzip -n ./checkpoints/BFM_Fitting.zip -d ./checkpoints/

### enhancer 
mkdir -p ./gfpgan/weights
curl -L --create-dirs https://github.com/xinntao/facexlib/releases/download/v0.1.0/alignment_WFLW_4HG.pth -o ./gfpgan/weights/alignment_WFLW_4HG.pth 
curl -L --create-dirs https://github.com/xinntao/facexlib/releases/download/v0.1.0/detection_Resnet50_Final.pth -o ./gfpgan/weights/detection_Resnet50_Final.pth 
curl -L --create-dirs https://github.com/TencentARC/GFPGAN/releases/download/v1.3.0/GFPGANv1.4.pth -o ./gfpgan/weights/GFPGANv1.4.pth 
curl -L --create-dirs https://github.com/xinntao/facexlib/releases/download/v0.2.2/parsing_parsenet.pth -o ./gfpgan/weights/parsing_parsenet.pth 

