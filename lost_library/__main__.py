"""Local command line entry point; every scientific output remains inspectable."""
from __future__ import annotations

import argparse
import functools
import http.server
import json
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser(description="The Lost Library local research pipeline")
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    sub = parser.add_subparsers(dest="command", required=True)
    ingest = sub.add_parser("ingest", help="Retrieve/cache a bounded, source-linked image sample")
    ingest.add_argument("--limit", type=int, default=120)
    ingest.add_argument("--offline", action="store_true")
    sub.add_parser("features", help="Extract interpretable layout and frozen pretrained visual features")
    sub.add_parser("evaluate", help="Evaluate against separated catalogue/literature reference labels")
    match = sub.add_parser("match", help="Rank compatibility candidates; scores do not prove identity")
    match.add_argument("--top-k", type=int, default=5)
    sub.add_parser("reconstruct", help="Build a documented partial-book demonstration with lacunae")
    sub.add_parser("export", help="Assemble local viewer data and evidence dossiers")
    sub.add_parser("evidence", help="Verify source regions and export the frozen evidence-review queue")
    knowledge = sub.add_parser("knowledge", help="Build, validate or export the manuscript-knowledge overlay without reranking")
    knowledge.add_argument("action", choices=["build", "validate", "export"])
    run = sub.add_parser("run", help="Run the complete research workflow, using cached data where possible")
    run.add_argument("--limit", type=int, default=120)
    run.add_argument("--offline", action="store_true")
    search = sub.add_parser("search", help="Search the local fragment database")
    search.add_argument("query")
    search.add_argument("--limit", type=int, default=20)
    serve = sub.add_parser("serve", help="Serve the local viewer on loopback only")
    serve.add_argument("--port", type=int, default=8765)
    args = parser.parse_args()
    root = args.root.resolve()
    if args.command == "knowledge":
        from .knowledge import build_knowledge, validate_knowledge, export_jsonld
        action = {"build": build_knowledge, "validate": validate_knowledge, "export": export_jsonld}[args.action]
        print(json.dumps(action(root), ensure_ascii=False, indent=2))
        return
    if args.command == "serve":
        handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=str(root))
        with http.server.ThreadingHTTPServer(("127.0.0.1", args.port), handler) as server:
            print(f"THE LOST LIBRARY: http://127.0.0.1:{args.port}/viewer/", flush=True)
            try:
                server.serve_forever()
            except KeyboardInterrupt:
                print("Local viewer stopped.")
        return
    if args.command in ("ingest", "run"):
        from .pipeline import ingest
        result = ingest(root, limit=args.limit, offline=args.offline)
        print(json.dumps(result, ensure_ascii=False, default=str))
    if args.command in ("features", "run"):
        from .vision import extract_features
        result = extract_features(root)
        print(json.dumps({"images_processed": result.get("images_processed"), "failed": result.get("failed"),
                          "encoder": result.get("encoder"), "details": "data/features.json"}, ensure_ascii=False, default=str))
    if args.command in ("evaluate", "run"):
        from .matching import evaluate
        result = evaluate(root)
        print(json.dumps({"sample_images": result.get("sample_images"), "sample_physical_objects": result.get("sample_physical_objects"),
                          "selection": result.get("selection"), "details": "data/validation.json"}, ensure_ascii=False, default=str))
    if args.command in ("match", "run"):
        from .matching import rank_candidates
        result = rank_candidates(root, top_k=getattr(args, "top_k", 5))
        print(json.dumps({"candidate_pairs": len(result), "details": "data/matches.json"}, ensure_ascii=False, default=str))
    if args.command in ("reconstruct", "run"):
        from .reconstruction import reconstruct
        print(json.dumps(reconstruct(root), ensure_ascii=False, default=str))
    if args.command in ("evidence", "run") and (root / "data/hypothesis_reviews.v1.json").exists():
        from .evidence import export_evidence
        print(json.dumps(export_evidence(root), ensure_ascii=False, default=str))
    if args.command in ("export", "run"):
        from .reconstruction import export_site
        print(json.dumps(export_site(root), ensure_ascii=False, default=str))
    if args.command == "search":
        from .pipeline import search
        print(json.dumps(search(root, args.query, limit=args.limit), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
