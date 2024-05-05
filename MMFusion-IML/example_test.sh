source data.sh
exp="./experiments/ec_example.yaml"
ckpt="./ckpt/late_fusion_localization.pth"
res="./results/ec_example/localization"
mkdir -p $res
$pint test_localization.py --exp $exp --ckpt $ckpt --manip $casiav2_manip > $res/Casiav2.txt