from magics.resources.chat import AsyncChat, Chat
from magics.resources.completions import AsyncCompletions, Completions
from magics.resources.embeddings import AsyncEmbeddings, Embeddings
from magics.resources.files import AsyncFiles, Files
from magics.resources.finetune import AsyncFineTuning, FineTuning
from magics.resources.images import AsyncImages, Images
from magics.resources.models import AsyncModels, Models
from magics.resources.rerank import AsyncRerank, Rerank
from magics.resources.resources import Resources
from magics.resources.gpus import GpuResource


__all__ = [
    "AsyncCompletions",
    "Completions",
    "AsyncChat",
    "Chat",
    "AsyncEmbeddings",
    "Embeddings",
    "AsyncFineTuning",
    "FineTuning",
    "AsyncFiles",
    "Files",
    "AsyncImages",
    "Images",
    "AsyncModels",
    "Models",
    "AsyncRerank",
    "Rerank",
    "Resources",
    "GpuResource",
]
