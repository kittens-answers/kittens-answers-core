import pytest

from kittens_answers_core.domain.entities import entities
from kittens_answers_core.domain.entities.enums import QuestionType


@pytest.fixture
def created_by():
    return entities.User(id=1, public_id="id")


# class TestMixin:
#     def test_id_mixin(self):
#         with pytest.raises(ValueError, match="id must be positive"):
#             entities.IDMixin(id=-1)


class TestUser:
    def test_empty_public_id(self):
        with pytest.raises(ValueError, match="public id can not be empty"):
            entities.User(id=1, public_id="")


class TestQuestion:
    @pytest.mark.parametrize(
        ["text", "question_type", "options", "extra_options"],
        (
            # ONE
            ("text", QuestionType.ONE, [], []),
            ("text", QuestionType.ONE, ["1", "2"], []),
            # MANY
            ("text", QuestionType.MANY, [], []),
            ("text", QuestionType.MANY, ["1", "2"], []),
            # ORDER
            ("text", QuestionType.ORDER, [], []),
            ("text", QuestionType.ORDER, ["1", "2"], []),
            # MATCH
            ("text", QuestionType.MATCH, [], []),
            ("text", QuestionType.MATCH, ["1", "2"], ["a", "b"]),
        ),
    )
    def test_correct(
        self,
        created_by: entities.User,
        text: str,
        question_type: QuestionType,
        options: list[str],
        extra_options: list[str],
    ):
        entities.Question(
            created_by=created_by,
            id=1,
            text=text,
            question_type=question_type,
            options=frozenset(options),
            extra_options=frozenset(extra_options),
        )

    @pytest.mark.parametrize(
        ["text", "question_type", "options", "extra_options"],
        (
            # ONE
            ("text", QuestionType.ONE, ["1"], []),
            ("text", QuestionType.ONE, ["1", "2"], ["a", "b"]),
            ("text", QuestionType.ONE, ["1"], ["a", "b"]),
            # MANY
            ("text", QuestionType.MANY, ["1"], []),
            ("text", QuestionType.MANY, ["1"], ["a", "b"]),
            ("text", QuestionType.MANY, ["1", "2"], ["a", "b"]),
            ("text", QuestionType.MANY, ["1", "2"], ["a"]),
            # ORDER
            ("text", QuestionType.ORDER, ["1"], []),
            ("text", QuestionType.ORDER, ["1"], ["b"]),
            ("text", QuestionType.ORDER, ["1", "2"], ["a"]),
            ("text", QuestionType.ORDER, ["1", "2"], ["a", "b"]),
            # MATCH
            ("text", QuestionType.MATCH, ["1"], []),
            ("text", QuestionType.MATCH, ["1"], ["a"]),
            ("text", QuestionType.MATCH, ["1"], ["a", "b"]),
            ("text", QuestionType.MATCH, ["1", "2"], ["a", "b", "c"]),
            ("text", QuestionType.MATCH, ["1", "2"], ["a"]),
            ("text", QuestionType.MATCH, ["1", "2"], []),
        ),
    )
    def test_incorrect(
        self,
        created_by: entities.User,
        text: str,
        question_type: QuestionType,
        options: list[str],
        extra_options: list[str],
    ):
        with pytest.raises(ValueError, match="options is inconsistent"):
            entities.Question(
                created_by=created_by,
                id=1,
                text=text,
                question_type=question_type,
                options=frozenset(options),
                extra_options=frozenset(extra_options),
            )

    def test_empty_text(self, created_by: entities.User):
        with pytest.raises(ValueError, match="text can not be empty"):
            entities.Question(
                created_by=created_by,
                id=1,
                text="",
                question_type=QuestionType.ONE,
            )


# class TestOneAnswer:
#     def test_correct(self):
#         entities.OneAnswer(id=1, value="1")
#         with pytest.raises(ValueError, match="answer can not be empty"):
#             entities.OneAnswer(id=1, value="")

#     def test_incorrect(self):
#         with pytest.raises(ValueError, match="answer can not be empty"):
#             entities.OneAnswer(id=1, value="")


# class TestManyAnswer:
#     def test_correct(self):
#         entities.ManyAnswer(id=1, value=frozenset(["1", "2"]))

#     def test_empty(self):
#         with pytest.raises(ValueError, match="answer can not be empty"):
#             entities.ManyAnswer(id=1, value=frozenset(["1", ""]))

#     @pytest.mark.parametrize(
#         "value",
#         [
#             [],
#         ],
#     )
#     def test_incorrect(self, value: list[str]):
#         with pytest.raises(ValueError, match="many answer must be one or more long"):
#             entities.ManyAnswer(id=1, value=frozenset(value))


# class TestOrderAnswer:
#     def test_correct(self):
#         entities.OrderAnswer(id=1, value=("1", "2"))

#     def test_empty(self):
#         with pytest.raises(ValueError, match="answer can not be empty"):
#             entities.OrderAnswer(id=1, value=("1", ""))

#     @pytest.mark.parametrize("value", [tuple(), ("1",)])
#     def test_incorrect(self, value: tuple[str, ...]):
#         with pytest.raises(ValueError, match="order answer must be two or more long"):
#             entities.OrderAnswer(id=1, value=value)


# class TestMatchAnswer:
#     def test_correct(self):
#         entities.MatchAnswer(id=1, value={"1": "a", "2": "b"})

#     @pytest.mark.parametrize("value", [{"": "a", "2": "b"}, {"1": "", "2": "b"}])
#     def test_empty(self, value: dict[str, str]):
#         with pytest.raises(ValueError, match="answer can not be empty"):
#             entities.MatchAnswer(id=1, value=value)

#     @pytest.mark.parametrize("value", [dict(), {"1": "a"}])
#     def test_incorrect(self, value: dict[str, str]):
#         with pytest.raises(ValueError, match="match answer must be two or more long"):
#             entities.MatchAnswer(id=1, value=value)


# class TestQuestionWithOneAnswer:
#     def test_correct(self, created_by: entities.User):
#         entities.QuestionWithAnswer(
#             question=entities.Question(created_by=created_by, id=1, question_type=QuestionType.ONE, text="?"),
#             answer=entities.OneAnswer(id=1, value="1"),
#         )
#         entities.QuestionWithAnswer(
#             question=entities.Question(
#                 created_by=created_by,
#                 id=1,
#                 question_type=QuestionType.ONE,
#                 text="?",
#                 options=frozenset(["1", "2"]),
#             ),
#             answer=entities.OneAnswer(id=1, value="1"),
#         )

#     def test_wrong_answer_type(self, created_by: entities.User):
#         with pytest.raises(ValueError, match="answer is inconsistent with question type"):
#             entities.QuestionWithAnswer(
#                 question=entities.Question(created_by=created_by, id=1, question_type=QuestionType.ONE, text="?"),
#                 answer=entities.ManyAnswer(id=1, value=frozenset(["1", "2"])),
#             )

#     def test_inconsistent_answer_value(self, created_by: entities.User):
#         with pytest.raises(ValueError, match="answer is inconsistent with question options"):
#             entities.QuestionWithAnswer(
#                 question=entities.Question(
#                     created_by=created_by,
#                     id=1,
#                     question_type=QuestionType.ONE,
#                     text="?",
#                     options=frozenset(["1", "2"]),
#                 ),
#                 answer=entities.OneAnswer(id=1, value="3"),
#             )


# class TestQuestionWithManyAnswer:
#     def test_correct(self, created_by: entities.User):
#         entities.QuestionWithAnswer(
#             question=entities.Question(created_by=created_by, id=1, question_type=QuestionType.MANY, text="?"),
#             answer=entities.ManyAnswer(id=1, value=frozenset(("1"))),
#         )
#         entities.QuestionWithAnswer(
#             question=entities.Question(
#                 created_by=created_by,
#                 id=1,
#                 question_type=QuestionType.MANY,
#                 text="?",
#                 options=frozenset(["1", "2"]),
#             ),
#             answer=entities.ManyAnswer(id=1, value=frozenset(("1",))),
#         )

#     def test_wrong_answer_type(self, created_by: entities.User):
#         with pytest.raises(ValueError, match="answer is inconsistent with question type"):
#             entities.QuestionWithAnswer(
#                 question=entities.Question(
#                     created_by=created_by,
#                     id=1,
#                     question_type=QuestionType.MANY,
#                     text="?",
#                 ),
#                 answer=entities.OneAnswer(id=1, value="1"),
#             )

#     def test_inconsistent_answer_value(self, created_by: entities.User):
#         with pytest.raises(ValueError, match="answer is inconsistent with question options"):
#             entities.QuestionWithAnswer(
#                 question=entities.Question(
#                     created_by=created_by,
#                     id=1,
#                     question_type=QuestionType.MANY,
#                     text="?",
#                     options=frozenset(["1", "2"]),
#                 ),
#                 answer=entities.ManyAnswer(id=1, value=frozenset(("3",))),
#             )


# class TestQuestionWithOrderAnswer:
#     def test_correct(self, created_by: entities.User):
#         entities.QuestionWithAnswer(
#             question=entities.Question(created_by=created_by, id=1, question_type=QuestionType.ORDER, text="?"),
#             answer=entities.OrderAnswer(id=1, value=("1", "2")),
#         )
#         entities.QuestionWithAnswer(
#             question=entities.Question(
#                 created_by=created_by,
#                 id=1,
#                 question_type=QuestionType.ORDER,
#                 text="?",
#                 options=frozenset(["1", "2"]),
#             ),
#             answer=entities.OrderAnswer(id=1, value=("2", "1")),
#         )

#     def test_wrong_answer_type(self, created_by: entities.User):
#         with pytest.raises(ValueError, match="answer is inconsistent with question type"):
#             entities.QuestionWithAnswer(
#                 question=entities.Question(
#                     created_by=created_by,
#                     id=1,
#                     question_type=QuestionType.ORDER,
#                     text="?",
#                 ),
#                 answer=entities.OneAnswer(id=1, value="1"),
#             )

#     def test_inconsistent_answer_value(self, created_by: entities.User):
#         with pytest.raises(ValueError, match="answer is inconsistent with question options"):
#             entities.QuestionWithAnswer(
#                 question=entities.Question(
#                     created_by=created_by,
#                     id=1,
#                     question_type=QuestionType.ORDER,
#                     text="?",
#                     options=frozenset(["1", "2"]),
#                 ),
#                 answer=entities.OrderAnswer(id=1, value=("1", "3")),
#             )


# class TestQuestionWithMatchAnswer:
#     def test_correct(self, created_by: entities.User):
#         entities.QuestionWithAnswer(
#             question=entities.Question(created_by=created_by, id=1, question_type=QuestionType.MATCH, text="?"),
#             answer=entities.MatchAnswer(id=1, value={"1": "b", "2": "a"}),
#         )
#         entities.QuestionWithAnswer(
#             question=entities.Question(
#                 created_by=created_by,
#                 id=1,
#                 question_type=QuestionType.MATCH,
#                 text="?",
#                 options=frozenset(["1", "2"]),
#                 extra_options=frozenset(["a", "b"]),
#             ),
#             answer=entities.MatchAnswer(id=1, value={"1": "a", "2": "b"}),
#         )

#     def test_wrong_answer_type(self, created_by: entities.User):
#         with pytest.raises(ValueError, match="answer is inconsistent with question type"):
#             entities.QuestionWithAnswer(
#                 question=entities.Question(
#                     created_by=created_by,
#                     id=1,
#                     question_type=QuestionType.MATCH,
#                     text="?",
#                 ),
#                 answer=entities.OneAnswer(id=1, value="1"),
#             )

#     @pytest.mark.parametrize(
#         "value",
#         [
#             {"1": "b", "2": "b"},
#             {"1": "b", "2": "c"},
#             {"1": "b", "2": "a", "3": "a"},
#         ],
#     )
#     def test_inconsistent_answer_value(self, created_by: entities.User, value: dict[str, str]):
#         with pytest.raises(ValueError, match="answer is inconsistent with question options"):
#             entities.QuestionWithAnswer(
#                 question=entities.Question(
#                     created_by=created_by,
#                     id=1,
#                     question_type=QuestionType.MATCH,
#                     text="?",
#                     options=frozenset(["1", "2"]),
#                     extra_options=frozenset(["a", "b"]),
#                 ),
#                 answer=entities.MatchAnswer(id=1, value=value),
#             )
