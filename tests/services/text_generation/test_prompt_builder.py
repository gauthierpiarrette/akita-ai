import pytest
from akita.services.text_generation.prompt_builder import PromptBuilder


class TestPromptBuilder:
    @pytest.fixture
    def setup_prompt_builder(self, tmp_path):
        # Setup a temporary directory for prompts
        d = tmp_path / "prompts"
        d.mkdir()
        p = d / "test_prompt.txt"
        p.write_text("This is a test prompt.")
        return PromptBuilder(prompts_dir=str(d))

    def test_init(self):
        pb = PromptBuilder("prompts")
        assert pb.prompts_dir == "prompts"
        assert pb.verbosity == "moderate"
        assert pb.language == "en"

    def test_get_prompt(self, setup_prompt_builder):
        pb = setup_prompt_builder
        prompt = pb.get_prompt("test", "Sample code content")
        assert "This is a test prompt." in prompt
        assert "Sample code content" in prompt

    def test_read_prompt_template_not_found(self, setup_prompt_builder):
        pb = setup_prompt_builder
        with pytest.raises(ValueError) as e:
            pb.get_prompt("nonexistent", "Sample code content")
        assert "was not found" in str(e.value)

    def test_build_prompt_different_verbosity(self, setup_prompt_builder):
        pb = setup_prompt_builder
        pb.verbosity = "high"
        high_verbosity_prompt = pb.get_prompt("test", "Sample code content")
        assert "very detailed and specific output" in high_verbosity_prompt

        pb.verbosity = "low"
        low_verbosity_prompt = pb.get_prompt("test", "Sample code content")
        assert "keep the output brief" in low_verbosity_prompt

    def test_build_prompt_different_language(self, setup_prompt_builder):
        pb = setup_prompt_builder
        pb.language = "fr"
        prompt = pb.get_prompt("test", "Sample code content")
        assert "Please translate the output to fr." in prompt

        pb.language = "en"
        prompt = pb.get_prompt("test", "Sample code content")
        assert "Please translate the output to" not in prompt
