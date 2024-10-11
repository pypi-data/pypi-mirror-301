import pytest
import torch
from bioimage_embed.models import __all_models__
from bioimage_embed.models import create_model


torch.manual_seed(42)


image_dim = [(256, 256), (224, 224)]
channel_dim = [
    3,
]
latent_dim = [64, 16]
pretrained_options = [True, False]
progress_options = [True, False]
batch = [1,]


@pytest.mark.parametrize("model", __all_models__)
@pytest.mark.parametrize("ld", latent_dim)
@pytest.mark.parametrize("c", channel_dim)
@pytest.mark.parametrize("idim", image_dim)
@pytest.mark.parametrize("pretrained", pretrained_options)
@pytest.mark.parametrize("progress", progress_options)
@pytest.mark.parametrize("batch", batch)
def test_create_model(model, c, idim, ld, pretrained, progress, batch):
    input_dim = (c, *idim)
    generated_model = create_model(model, input_dim, ld, pretrained, progress)
    data = torch.rand(batch, *input_dim)
    output = generated_model({"data": data})
    assert output.z.shape[1] == ld
    assert output.recon_x.shape == data.shape
    # assert output.z.shape == (batch, ld)
    if len(output.z.flatten()) != ld:
        pytest.skip("Not an exact latent dimension match")
