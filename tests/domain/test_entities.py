import pytest

from kittens_answers_core.domain import entities


@pytest.fixture
def created_by():
    return entities.User(id=1, public_id="id").id


class TestUser:
    def test_empty_public_id(self):
        with pytest.raises(ValueError, match="public id can not be empty"):
            entities.User(id=1, public_id="")


class TestQuestion:
    @pytest.mark.parametrize(
        ["text", "question_type", "options", "extra_options"],
        (
            # ONE
            ("text", entities.QuestionType.ONE, [], []),
            ("text", entities.QuestionType.ONE, ["1", "2"], []),
            # MANY
            ("text", entities.QuestionType.MANY, [], []),
            ("text", entities.QuestionType.MANY, ["1", "2"], []),
            # ORDER
            ("text", entities.QuestionType.ORDER, [], []),
            ("text", entities.QuestionType.ORDER, ["1", "2"], []),
            # MATCH
            ("text", entities.QuestionType.MATCH, [], []),
            ("text", entities.QuestionType.MATCH, ["1", "2"], ["a", "b"]),
        ),
    )
    def test_correct(
        self,
        created_by: entities.IDType,
        text: str,
        question_type: entities.QuestionType,
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
            ("text", entities.QuestionType.ONE, ["1"], []),
            ("text", entities.QuestionType.ONE, ["1", "2"], ["a", "b"]),
            ("text", entities.QuestionType.ONE, ["1"], ["a", "b"]),
            # MANY
            ("text", entities.QuestionType.MANY, ["1"], []),
            ("text", entities.QuestionType.MANY, ["1"], ["a", "b"]),
            ("text", entities.QuestionType.MANY, ["1", "2"], ["a", "b"]),
            ("text", entities.QuestionType.MANY, ["1", "2"], ["a"]),
            # ORDER
            ("text", entities.QuestionType.ORDER, ["1"], []),
            ("text", entities.QuestionType.ORDER, ["1"], ["b"]),
            ("text", entities.QuestionType.ORDER, ["1", "2"], ["a"]),
            ("text", entities.QuestionType.ORDER, ["1", "2"], ["a", "b"]),
            # MATCH
            ("text", entities.QuestionType.MATCH, ["1"], []),
            ("text", entities.QuestionType.MATCH, ["1"], ["a"]),
            ("text", entities.QuestionType.MATCH, ["1"], ["a", "b"]),
            ("text", entities.QuestionType.MATCH, ["1", "2"], ["a", "b", "c"]),
            ("text", entities.QuestionType.MATCH, ["1", "2"], ["a"]),
            ("text", entities.QuestionType.MATCH, ["1", "2"], []),
        ),
    )
    def test_incorrect(
        self,
        created_by: entities.IDType,
        text: str,
        question_type: entities.QuestionType,
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

    def test_empty_text(self, created_by: entities.IDType):
        with pytest.raises(ValueError, match="text can not be empty"):
            entities.Question(
                created_by=created_by,
                id=1,
                text="",
                question_type=entities.QuestionType.ONE,
            )

    def test_empty_options(self, created_by: entities.IDType):
        with pytest.raises(ValueError, match="options or extra options can not be empty"):
            entities.Question(
                created_by=created_by,
                id=1,
                text="?",
                question_type=entities.QuestionType.ONE,
                options=frozenset(("", "1")),
            )

        with pytest.raises(ValueError, match="options or extra options can not be empty"):
            entities.Question(
                created_by=created_by,
                id=1,
                text="?",
                question_type=entities.QuestionType.MATCH,
                options=frozenset(("1", "2")),
                extra_options=frozenset(("a", "")),
            )


class TestOneAnswer:
    def test_correct(self, created_by: entities.IDType):
        entities.OneAnswer(id=1, value="1", created_by=created_by, question_id=1)
        with pytest.raises(ValueError, match="answer can not be empty"):
            entities.OneAnswer(id=1, value="", created_by=created_by, question_id=1)

    def test_incorrect(self, created_by: entities.IDType):
        with pytest.raises(ValueError, match="answer can not be empty"):
            entities.OneAnswer(id=1, value="", created_by=created_by, question_id=1)


class TestManyAnswer:
    def test_correct(self, created_by: entities.IDType):
        entities.ManyAnswer(id=1, value=frozenset(["1", "2"]), created_by=created_by, question_id=1)

    def test_empty(self, created_by: entities.IDType):
        with pytest.raises(ValueError, match="answer can not be empty"):
            entities.ManyAnswer(id=1, value=frozenset(["1", ""]), created_by=created_by, question_id=1)

    @pytest.mark.parametrize(
        "value",
        [
            [],
        ],
    )
    def test_incorrect(self, value: list[str], created_by: entities.IDType):
        with pytest.raises(ValueError, match="many answer must be one or more long"):
            entities.ManyAnswer(id=1, value=frozenset(value), created_by=created_by, question_id=1)


class TestOrderAnswer:
    def test_correct(self, created_by: entities.IDType):
        entities.OrderAnswer(id=1, value=("1", "2"), created_by=created_by, question_id=1)

    def test_empty(self, created_by: entities.IDType):
        with pytest.raises(ValueError, match="answer can not be empty"):
            entities.OrderAnswer(id=1, value=("1", ""), created_by=created_by, question_id=1)

    @pytest.mark.parametrize("value", [tuple(), ("1",)])
    def test_incorrect(self, value: tuple[str, ...], created_by: entities.IDType):
        with pytest.raises(ValueError, match="order answer must be two or more long"):
            entities.OrderAnswer(id=1, value=value, created_by=created_by, question_id=1)


class TestMatchAnswer:
    def test_correct(self, created_by: entities.IDType):
        entities.MatchAnswer(id=1, value={"1": "a", "2": "b"}, created_by=created_by, question_id=1)

    @pytest.mark.parametrize("value", [{"": "a", "2": "b"}, {"1": "", "2": "b"}])
    def test_empty(self, value: dict[str, str], created_by: entities.IDType):
        with pytest.raises(ValueError, match="answer can not be empty"):
            entities.MatchAnswer(id=1, value=value, created_by=created_by, question_id=1)

    @pytest.mark.parametrize("value", [dict(), {"1": "a"}])
    def test_incorrect(self, value: dict[str, str], created_by: entities.IDType):
        with pytest.raises(ValueError, match="match answer must be two or more long"):
            entities.MatchAnswer(id=1, value=value, created_by=created_by, question_id=1)


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
