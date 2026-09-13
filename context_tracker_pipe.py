"""
title: Hardcore-Henry Custom Triage Pipe
author: Corey Westrem
version: 1.2.6
license: MIT
description: Standalone custom proxy pipe that features a fully functional filling dot token meter with historical badge stripping.
"""

import requests
from typing import List, Dict, Generator, Union

class Pipe:
    def __init__(self):
        self.valves = {
            "OLLAMA_HOST": "http://172.17.0.1:11434",
            "MODEL_NAME": "hardcore-henry:latest",
            "MAX_CONTEXT": 16384
        }

    def _estimate_tokens(self, text: str) -> int:
        if not text:
            return 0
        return len(text) // 4

    def pipes(self) -> List[Dict[str, str]]:
        return [{"id": "hardcore_henry_triage", "name": "Hardcore-Henry (with Context Counter)"}]

    def pipe(self, body: dict) -> Union[str, Generator]:
        try:
            messages = body.get("messages", [])
            formatted_messages = []
            cumulative_tokens = 0

            for msg in messages:
                role = msg.get("role", "user")
                raw_content = msg.get("content", "")
                
                clean_content = ""
                clean_images = []

                if isinstance(raw_content, list):
                    for item in raw_content:
                        if item.get("type") == "text":
                            txt = item.get("text", "")
                            if "Session Context:" in txt:
                                txt = txt.split("\n\n***\n")
                            clean_content += txt
                        elif item.get("type") == "image_url":
                            img_url = item.get("image_url", {}).get("url", "")
                            if "base64," in img_url:
                                img_url = img_url.split("base64,")[-1]
                            clean_images.append(img_url)
                            cumulative_tokens += 1024
                else:
                    clean_content = str(raw_content)
                    if "Session Context:" in clean_content:
                        clean_content = clean_content.split("\n\n***\n")

                cumulative_tokens += self._estimate_tokens(clean_content)
                clean_msg = {"role": role, "content": clean_content}

                root_images = msg.get("images") or []
                for img in root_images:
                    if isinstance(img, str) and "base64," in img:
                        img = img.split("base64,")[-1]
                    if img not in clean_images:
                        clean_images.append(img)
                        cumulative_tokens += 1024

                if clean_images and role == "user":
                    clean_msg["images"] = clean_images

                formatted_messages.append(clean_msg)

            ollama_url = f"{self.valves['OLLAMA_HOST']}/api/chat"
            payload = {
                "model": self.valves["MODEL_NAME"],
                "messages": formatted_messages,
                "stream": False
            }

            response = requests.post(ollama_url, json=payload, timeout=120)
            response.raise_for_status()

            henry_response = response.json().get("message", {}).get("content", "")
            cumulative_tokens += self._estimate_tokens(henry_response)
            
            max_ctx = self.valves["MAX_CONTEXT"]
            pct = (cumulative_tokens / max_ctx) * 100 if max_ctx > 0 else 0

            filled_bars = min(5, int((pct / 100) * 5))
            if cumulative_tokens > 0 and filled_bars == 0:
                filled_bars = 1
                
            bar_str = "[" + "⬢" * filled_bars + "⬡" * (5 - filled_bars) + "]"
            
            tracker_badge = f"\n\n***\n{bar_str} **Session Context:** {cumulative_tokens:,} / {max_ctx:,} ({pct:.1f}%)"

            return henry_response + tracker_badge

        except Exception as e:
            return f"Hardcore-Henry Pipe Error: Network conversion fault. Details: {str(e)}"

