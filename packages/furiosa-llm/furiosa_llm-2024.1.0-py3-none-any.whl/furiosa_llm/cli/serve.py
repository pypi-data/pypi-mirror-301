from furiosa_llm.server.app import run_server


def add_serve_args(serve_parser):
    serve_parser.add_argument(
        "--model",
        type=str,
        required=True,
        help="The Hugging Face model id, or path to Furiosa model artifact. Currently only one model is supported per server.",
    )
    serve_parser.add_argument(
        "--host",
        default="0.0.0.0",
        help="Host to bind the server to",
    )
    serve_parser.add_argument(
        "--port",
        type=int,
        default=8000,
        help="Port to bind the server to",
    )
    serve_parser.add_argument(
        "--chat-template",
        type=str,
        required=True,
        help="Path to chat template file (must be a jinja2 template)",
    )
    serve_parser.add_argument(
        "--response-role",
        type=str,
        default="assistant",
        help="Response role for /v1/chat/completions API (default: 'assistant')",
    )
    serve_parser.add_argument(
        "-tp",
        "--tensor-parallel-size",
        type=int,
        help="Number of tensor parallel replicas. (default: 4)",
    )
    serve_parser.add_argument(
        "-pp",
        "--pipeline-parallel-size",
        type=int,
        help="Number of pipeline stages. (default: 1)",
    )
    serve_parser.add_argument(
        "-dp",
        "--data-parallel-size",
        type=int,
        help="Data parallelism size. If not given, it will be inferred from total avaialble PEs and other parallelism degrees.",
    )
    serve_parser.add_argument(
        "--devices",
        type=str,
        default=None,
        help='Devices to use (e.g. "npu:0:*,npu:1:*"). If unspecified, all available devices from the host will be used.',
    )
    serve_parser.set_defaults(dispatch_function=serve)


def serve(args):
    run_server(args)
