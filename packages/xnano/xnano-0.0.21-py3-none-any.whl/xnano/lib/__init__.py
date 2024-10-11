__all__ = [
    # llm
    "classifier",
    "coder",
    "extractor",
    "function",
    "generator",
    "validator",
    "planner",
    "prompter",
    "qa",
    "solver",
    "query",

    # nlp/data
    "chunker",
    "reader",

    # multimodal
    "image",
    "audio",
    "transcribe"
]


from .._router import router


class classifier(router):
    pass


classifier.init("xnano.lib.classify", "classifier")


class coder(router):
    pass

coder.init("xnano.lib.code", "coder")


class extractor(router):
    pass

extractor.init("xnano.lib.extract", "extractor")


class function(router):
    pass


function.init("xnano.lib.function_constructor", "function")


class generator(router):
    pass

generator.init("xnano.lib.generate", "generator")


class validator(router):
    pass


validator.init("xnano.lib.validate", "validator")


class planner(router):
    pass


planner.init("xnano.lib.plan", "planner")


class prompter(router):
    pass


prompter.init("xnano.lib.prompt", "prompter")


class qa(router):
    pass

qa.init("xnano.lib.question_answer", "qa")


class solver(router):
    pass


solver.init("xnano.lib.solve", "solver")


class query(router):
    pass


query.init("xnano.lib.query", "query")


class chunker(router):
    pass


chunker.init("xnano.lib.chunk", "chunker")


class reader(router):
    pass


reader.init("xnano.lib.read", "reader")


class image(router):
    pass


image.init("xnano.lib.multimodal", "image")


class audio(router):
    pass


audio.init("xnano.lib.multimodal", "audio")


class transcribe(router):
    pass


transcribe.init("xnano.lib.multimodal", "transcribe")







