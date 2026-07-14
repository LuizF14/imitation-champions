import json
import random
import statistics
from dataclasses import dataclass, field, asdict, is_dataclass  # Adicionado is_dataclass
from pathlib import Path

from agents.judge_agent import JudgeAgent
from agents.interrogator_agent import InterrogatorAgent
from services.conversation_service import ConversationService
from schemas.judge_verdict import JudgeVerdict


@dataclass
class Turn:
    speaker: str  # "I" ou "W"
    content: str


@dataclass
class BenchmarkRun:
    thread_id: str
    transcript: str
    verdict: JudgeVerdict
    fooled_judge: bool

    def to_dict(self):
        # Resolve o problema de tentar usar asdict() em modelos Pydantic
        if hasattr(self.verdict, "model_dump"):
            verdict_dict = self.verdict.model_dump()
        elif hasattr(self.verdict, "dict"):
            verdict_dict = self.verdict.dict()
        elif is_dataclass(self.verdict):
            verdict_dict = asdict(self.verdict)
        else:
            verdict_dict = self.verdict

        return {
            "thread_id": self.thread_id,
            "transcript": self.transcript,
            "verdict": verdict_dict,
            "fooled_judge": self.fooled_judge,
        }


@dataclass
class BenchmarkResult:
    runs: list[BenchmarkRun] = field(default_factory=list)

    @property
    def win_rate(self) -> float:
        if not self.runs:
            return 0.0
        return sum(r.fooled_judge for r in self.runs) / len(self.runs)

    @property
    def avg_confidence(self) -> float:
        if not self.runs:
            return 0.0
        return statistics.mean(r.verdict.confidence for r in self.runs)

    def summary(self) -> str:
        return "\n".join([
            f"Conversas avaliadas: {len(self.runs)}",
            f"Taxa de sucesso (bot passou por humano): {self.win_rate:.1%}",
            f"Confiança média do judge: {self.avg_confidence:.1f}",
        ])

    def to_dict(self):
        return {
            "summary": {
                "n_conversations": len(self.runs),
                "win_rate": self.win_rate,
                "avg_confidence": self.avg_confidence,
            },
            "runs": [run.to_dict() for run in self.runs],
        }

    def save_json(self, filename: str | Path):
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(
                self.to_dict(),
                f,
                ensure_ascii=False,
                indent=4,
            )


class JudgmentService:
    def __init__(self):
        self.judge = JudgeAgent()
        self.interrogator = InterrogatorAgent()

    def run_benchmark(
        self,
        n_conversations: int = 10,
        turns_per_conversation: int = 4,
        output_file: str = "benchmark_results.json",
    ) -> BenchmarkResult:

        result = BenchmarkResult()

        for i in range(n_conversations):
            thread_id = f"benchmark-{i}-{random.randint(1000, 9999)}"

            turns = self._simulate_conversation(
                thread_id,
                turns_per_conversation,
            )

            transcript = self._format_transcript(turns)

            verdict = self.judge.run(transcript)

            result.runs.append(
                BenchmarkRun(
                    thread_id=thread_id,
                    transcript=transcript,
                    verdict=verdict,
                    fooled_judge=(verdict.verdict == "humano"),
                )
            )

            print(
                f"[{i+1}/{n_conversations}] "
                f"veredito={verdict.verdict} "
                f"confianca={verdict.confidence}"
            )

        result.save_json(output_file)

        print(f"\nResultados salvos em: {output_file}")

        return result

    def _simulate_conversation(
        self,
        thread_id: str,
        n_turns: int,
    ) -> list[Turn]:

        conversation_service = ConversationService()
        turns: list[Turn] = []

        for _ in range(n_turns):
            transcript_so_far = self._format_transcript(turns)

            question = self.interrogator.run(transcript_so_far)
            turns.append(Turn("I", question))

            result = conversation_service.execute(question, thread_id)

            for response in result.messages:
                turns.append(Turn("W", response))

        return turns

    def _format_transcript(self, turns: list[Turn]) -> str:
        return "\n".join(
            f"{turn.speaker}: {turn.content}"
            for turn in turns
        )