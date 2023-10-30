from mimesis.providers import BaseProvider, Text

from kittens_answers_core.models import Question, QuestionTypes


class AnswerProvider(BaseProvider):
    class Meta:  # pyright: ignore [reportIncompatibleVariableOverride]
        name = "QA"

    def question_type(self, question_type: QuestionTypes | None) -> QuestionTypes:
        if question_type:
            return question_type
        else:
            return self.random.choice_enum_item(QuestionTypes)

    def options(self) -> set[str]:
        return set(Text().words())

    def extra_options(self, question_type: QuestionTypes) -> set[str]:
        if question_type == QuestionTypes.MATCH:
            return set(Text().words())
        else:
            return set()

    def answer(self, question: Question) -> list[str]:
        match question.question_type:
            case QuestionTypes.ONE:
                if question.options:
                    return [self.random.choice(list(question.options))]
                else:
                    return Text().words(quantity=1)
            case QuestionTypes.MANY:
                if question.options:
                    return self.random.sample(
                        list(question.options), k=self.random.choice(range(1, len(question.options) + 1))
                    )
                else:
                    return Text().words()
            case QuestionTypes.ORDER | QuestionTypes.MATCH:
                if question.options:
                    _answer = list(question.options)
                    self.random.shuffle(_answer)
                    return _answer
                else:
                    return Text().words()
        raise ValueError

    def extra_answer(self, question: Question) -> list[str]:
        if question.question_type == QuestionTypes.MATCH:
            if question.extra_options:
                _extra_answer = list(question.extra_options)
                self.random.shuffle(_extra_answer)
                return _extra_answer
            else:
                return Text().words()
        else:
            return []

    def is_correct(self) -> bool:
        return self.random.choice([True, False])
