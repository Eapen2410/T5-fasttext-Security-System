
import fasttext

model = fasttext.train_supervised(
    input="train.txt",
    dim=100,
    lr=0.3,
    epoch=25,
    wordNgrams=2,

    loss='softmax'
)

model.save_model("query_sensitivity_model.ftz")
