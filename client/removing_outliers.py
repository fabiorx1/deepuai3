import sys, os, shutil
from sklearn.ensemble import IsolationForest

sys.path.append('.')
from models.mlns.outlier import DeepUaiOutlierDetection
from models import DeepUaiDataset

wav_inliers_ds_name = 'deglut-audios-wav-inliers'
wav_inliers_ds_path = DeepUaiDataset._get_path(wav_inliers_ds_name)
if not os.path.exists(wav_inliers_ds_path): os.makedirs(wav_inliers_ds_path)

clf = IsolationForest(contamination=.5)
deepuai = DeepUaiOutlierDetection(clf=clf, name='iforest-standand',
                                  ds_name='deglut-audios-statistics2')
y = deepuai.execute()
stats_inliers_ds = deepuai.create_inliers_ds()

wav_ds = DeepUaiDataset('deglut-audios-wav')
inliers_fnames = [os.path.basename(fpath).split('.')[0]
                  for fpath in stats_inliers_ds.filepaths]

for fpath in wav_ds.filepaths:
    basename = os.path.basename(fpath)
    fname = basename.split('.')[0]
    if fname in inliers_fnames:
        shutil.copyfile(fpath, os.path.join(wav_inliers_ds_path, basename))