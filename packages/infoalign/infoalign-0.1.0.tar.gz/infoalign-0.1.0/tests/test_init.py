from src.representer import InfoAlignRepresenter

model = InfoAlignRepresenter(model_path='infoalign_model/pretrain.pt')

representations = model.predict('CCC')
print(representations)