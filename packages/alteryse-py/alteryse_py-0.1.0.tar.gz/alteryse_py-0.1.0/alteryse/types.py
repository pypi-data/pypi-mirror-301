from typing import List, Optional
from dataclasses import dataclass

@dataclass
class GenerateResponse:
    content: str

@dataclass
class ChatMessage:
    role: str  # 'system' | 'user' | 'assistant'
    content: str
    images: Optional[List[str]] = None

@dataclass
class ChatRequest:
    messages: List[ChatMessage]

@dataclass
class ChatResponse:
    content: str

@dataclass
class Options:
    numa: Optional[bool] = None
    num_ctx: Optional[int] = None
    num_batch: Optional[int] = None
    logits_all: Optional[bool] = None
    vocab_only: Optional[bool] = None
    num_thread: Optional[int] = None
    num_keep: Optional[int] = None
    seed: Optional[int] = None
    num_predict: Optional[int] = None
    top_k: Optional[int] = None
    top_p: Optional[float] = None
    tfs_z: Optional[float] = None
    typical_p: Optional[float] = None
    repeat_last_n: Optional[int] = None
    temperature: Optional[float] = None
    repeat_penalty: Optional[float] = None
    presence_penalty: Optional[float] = None
    frequency_penalty: Optional[float] = None
    mirostat: Optional[float] = None
    mirostat_tau: Optional[float] = None
    mirostat_eta: Optional[float] = None
    penalize_newline: Optional[bool] = None
    stop: Optional[List[str]] = None
