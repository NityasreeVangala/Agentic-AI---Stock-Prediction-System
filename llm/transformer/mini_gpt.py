# llm/transformer/mini_gpt.py

import torch
import torch.nn as nn
import torch.nn.functional as F

# Assume vocab_size, block_size, embed_dim are set globally or passed as args
# You can load them from your saved model

class TransformerBlock(nn.Module):
    def __init__(self, embed_dim=128, num_heads=4, dropout=0.1):
        super().__init__()
        self.ln1 = nn.LayerNorm(embed_dim)
        self.attn = nn.MultiheadAttention(embed_dim, num_heads, dropout=dropout, batch_first=True)
        self.ln2 = nn.LayerNorm(embed_dim)
        self.ff = nn.Sequential(
            nn.Linear(embed_dim, 4*embed_dim),
            nn.ReLU(),
            nn.Linear(4*embed_dim, embed_dim),
            nn.Dropout(dropout)
        )

    def forward(self, x):
        attn_out, _ = self.attn(x, x, x, need_weights=False)
        x = self.ln1(x + attn_out)
        x = self.ln2(x + self.ff(x))
        return x


class MiniGPT(nn.Module):
    def __init__(self, vocab_size, embed_dim=128, block_size=64, num_layers=4):
        super().__init__()
        self.embed = nn.Embedding(vocab_size, embed_dim)
        self.pos_embed = nn.Embedding(block_size, embed_dim)
        self.blocks = nn.Sequential(*[TransformerBlock(embed_dim=embed_dim) for _ in range(num_layers)])
        self.ln = nn.LayerNorm(embed_dim)
        self.head = nn.Linear(embed_dim, vocab_size)

    def forward(self, idx):
        B, T = idx.shape
        pos = torch.arange(T, device=idx.device)
        x = self.embed(idx) + self.pos_embed(pos)
        x = self.blocks(x)
        x = self.ln(x)
        return self.head(x)

    def generate(self, prompt_idx, max_len=300, temperature=0.8):
        self.eval()
        idx = prompt_idx
        for _ in range(max_len):
            idx_cond = idx[:, -64:]  # last block_size tokens
            logits = self(idx_cond)
            probs = F.softmax(logits[:, -1, :] / temperature, dim=-1)
            next_idx = torch.multinomial(probs, num_samples=1)
            idx = torch.cat([idx, next_idx], dim=1)
        return idx
