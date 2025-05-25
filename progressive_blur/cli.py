"""
Command-line interface for progressive blur operations.
"""

import argparse
import sys
from pathlib import Path
from typing import Optional

from .core import BlurDirection, BlurAlgorithm, EasingFunction, apply_progressive_blur
from .utils import (
    batch_process_images,
    apply_preset,
    BLUR_PRESETS,
    get_image_info,
    is_supported_format,
)


def create_parser() -> argparse.ArgumentParser:
    """Create the argument parser for the CLI."""
    parser = argparse.ArgumentParser(
        prog="progressive-blur",
        description="Apply progressive blur effects to images",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Apply default blur to a single image
  progressive-blur input.jpg output.jpg

  # Use a preset
  progressive-blur input.jpg output.jpg --preset dramatic

  # Custom blur parameters
  progressive-blur input.jpg output.jpg --max-blur 30 --direction left_to_right

  # Batch process a directory
  progressive-blur --batch input_dir/ output_dir/

  # Get image information
  progressive-blur --info image.jpg
        """,
    )

    # Main operation mode
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "input",
        nargs="?",
        help="Input image file or directory (for batch processing)",
    )
    group.add_argument(
        "--info",
        metavar="IMAGE",
        help="Show information about an image file",
    )
    group.add_argument(
        "--list-presets",
        action="store_true",
        help="List available blur presets",
    )

    # Output
    parser.add_argument(
        "output",
        nargs="?",
        help="Output image file or directory (for batch processing)",
    )

    # Batch processing
    parser.add_argument(
        "--batch",
        action="store_true",
        help="Enable batch processing mode",
    )
    parser.add_argument(
        "--recursive",
        action="store_true",
        help="Process subdirectories recursively (batch mode only)",
    )
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="Overwrite existing output files",
    )
    parser.add_argument(
        "--prefix",
        default="blurred_",
        help="Prefix for output filenames in batch mode (default: blurred_)",
    )

    # Blur parameters
    parser.add_argument(
        "--preset",
        choices=list(BLUR_PRESETS.keys()),
        help="Use a predefined blur preset",
    )
    parser.add_argument(
        "--max-blur",
        type=float,
        default=50.0,
        help="Maximum blur radius (default: 50.0)",
    )
    parser.add_argument(
        "--clear-until",
        type=float,
        default=0.15,
        help="Percentage to keep completely clear (default: 0.15)",
    )
    parser.add_argument(
        "--blur-start",
        type=float,
        default=0.25,
        help="Percentage where blur starts (default: 0.25)",
    )
    parser.add_argument(
        "--end-position",
        type=float,
        default=0.85,
        help="Percentage where maximum blur is reached (default: 0.85)",
    )
    parser.add_argument(
        "--direction",
        choices=[d.value for d in BlurDirection],
        default=BlurDirection.TOP_TO_BOTTOM.value,
        help="Direction of the blur effect (default: top_to_bottom)",
    )
    parser.add_argument(
        "--algorithm",
        choices=[a.value for a in BlurAlgorithm],
        default=BlurAlgorithm.GAUSSIAN.value,
        help="Blur algorithm to use (default: gaussian)",
    )
    parser.add_argument(
        "--easing",
        choices=[e.value for e in EasingFunction],
        default=EasingFunction.LINEAR.value,
        help="Easing function for blur transition (default: linear)",
    )
    parser.add_argument(
        "--no-preserve-alpha",
        action="store_true",
        help="Don't preserve alpha channel",
    )

    # Output options
    parser.add_argument(
        "--quality",
        type=int,
        default=95,
        help="JPEG/WebP quality (1-100, default: 95)",
    )

    # Verbosity
    parser.add_argument(
        "--verbose",
        "-v",
        action="store_true",
        help="Enable verbose output",
    )
    parser.add_argument(
        "--quiet",
        "-q",
        action="store_true",
        help="Suppress all output except errors",
    )

    return parser


def validate_args(args: argparse.Namespace) -> None:
    """Validate command-line arguments."""
    if args.list_presets or args.info:
        return

    if not args.input:
        raise ValueError("Input file or directory is required")

    if not args.batch and not args.output:
        raise ValueError("Output file is required for single image processing")

    if args.batch and not args.output:
        raise ValueError("Output directory is required for batch processing")

    # Validate percentage values
    for param, value in [
        ("clear-until", args.clear_until),
        ("blur-start", args.blur_start),
        ("end-position", args.end_position),
    ]:
        if not 0.0 <= value <= 1.0:
            raise ValueError(f"{param} must be between 0.0 and 1.0")

    # Validate parameter relationships
    if args.clear_until >= args.blur_start:
        raise ValueError("clear-until must be less than blur-start")
    if args.blur_start >= args.end_position:
        raise ValueError("blur-start must be less than end-position")

    # Validate quality
    if not 1 <= args.quality <= 100:
        raise ValueError("Quality must be between 1 and 100")

    # Validate max blur
    if args.max_blur <= 0:
        raise ValueError("max-blur must be positive")


def progress_callback(current: int, total: int, input_path: Path, output_path: Path) -> None:
    """Progress callback for batch processing."""
    print(f"[{current}/{total}] {input_path.name} -> {output_path.name}")


def show_image_info(image_path: str) -> None:
    """Show information about an image file."""
    try:
        info = get_image_info(image_path)
        print(f"Image Information: {info['filename']}")
        print(f"  Format: {info['format']}")
        print(f"  Mode: {info['mode']}")
        print(f"  Size: {info['width']} x {info['height']} pixels")
        print(f"  Has transparency: {info['has_transparency']}")
        print(f"  File size: {info['file_size']:,} bytes")
    except Exception as e:
        print(f"Error reading image info: {e}", file=sys.stderr)
        sys.exit(1)


def list_presets() -> None:
    """List available blur presets."""
    print("Available blur presets:")
    print()
    for name, preset in BLUR_PRESETS.items():
        print(f"  {name}:")
        print(f"    Name: {preset['name']}")
        print(f"    Max blur: {preset['max_blur']}")
        print(f"    Direction: {preset['direction'].value}")
        print(f"    Algorithm: {preset['algorithm'].value}")
        print(f"    Easing: {preset['easing'].value}")
        print()


def process_single_image(args: argparse.Namespace) -> None:
    """Process a single image."""
    input_path = Path(args.input)
    output_path = Path(args.output)

    if not input_path.exists():
        print(f"Error: Input file not found: {input_path}", file=sys.stderr)
        sys.exit(1)

    if not is_supported_format(input_path):
        print(f"Error: Unsupported image format: {input_path.suffix}", file=sys.stderr)
        sys.exit(1)

    if not args.overwrite and output_path.exists():
        print(f"Error: Output file already exists: {output_path}", file=sys.stderr)
        print("Use --overwrite to overwrite existing files")
        sys.exit(1)

    try:
        if args.verbose:
            print(f"Processing: {input_path}")

        if args.preset:
            # Use preset
            result = apply_preset(
                str(input_path),
                args.preset,
                preserve_alpha=not args.no_preserve_alpha,
            )
        else:
            # Use custom parameters
            result = apply_progressive_blur(
                str(input_path),
                max_blur=args.max_blur,
                clear_until=args.clear_until,
                blur_start=args.blur_start,
                end_position=args.end_position,
                direction=args.direction,
                algorithm=args.algorithm,
                easing=args.easing,
                preserve_alpha=not args.no_preserve_alpha,
            )

        # Save result
        save_kwargs = {}
        if output_path.suffix.lower() in ('.jpg', '.jpeg'):
            save_kwargs['quality'] = args.quality
            save_kwargs['optimize'] = True
        elif output_path.suffix.lower() == '.webp':
            save_kwargs['quality'] = args.quality
            save_kwargs['method'] = 6
        elif output_path.suffix.lower() == '.png':
            save_kwargs['optimize'] = True

        result.save(output_path, **save_kwargs)

        if not args.quiet:
            print(f"Saved: {output_path}")

    except Exception as e:
        print(f"Error processing image: {e}", file=sys.stderr)
        sys.exit(1)


def process_batch(args: argparse.Namespace) -> None:
    """Process multiple images in batch mode."""
    input_dir = Path(args.input)
    output_dir = Path(args.output)

    if not input_dir.exists():
        print(f"Error: Input directory not found: {input_dir}", file=sys.stderr)
        sys.exit(1)

    if not input_dir.is_dir():
        print(f"Error: Input path is not a directory: {input_dir}", file=sys.stderr)
        sys.exit(1)

    try:
        if args.verbose:
            print(f"Processing directory: {input_dir}")
            print(f"Output directory: {output_dir}")

        # Prepare parameters
        if args.preset:
            preset = BLUR_PRESETS[args.preset]
            kwargs = {
                'max_blur': preset['max_blur'],
                'clear_until': preset['clear_until'],
                'blur_start': preset['blur_start'],
                'end_position': preset['end_position'],
                'direction': preset['direction'],
                'algorithm': preset['algorithm'],
                'easing': preset['easing'],
            }
        else:
            kwargs = {
                'max_blur': args.max_blur,
                'clear_until': args.clear_until,
                'blur_start': args.blur_start,
                'end_position': args.end_position,
                'direction': args.direction,
                'algorithm': args.algorithm,
                'easing': args.easing,
            }

        # Process images
        processed_files = batch_process_images(
            input_dir,
            output_dir,
            preserve_alpha=not args.no_preserve_alpha,
            recursive=args.recursive,
            overwrite=args.overwrite,
            quality=args.quality,
            prefix=args.prefix,
            progress_callback=progress_callback if args.verbose else None,
            **kwargs,
        )

        if not args.quiet:
            print(f"Processed {len(processed_files)} images")

    except Exception as e:
        print(f"Error in batch processing: {e}", file=sys.stderr)
        sys.exit(1)


def main() -> None:
    """Main entry point for the CLI."""
    parser = create_parser()
    args = parser.parse_args()

    try:
        # Handle special modes
        if args.list_presets:
            list_presets()
            return

        if args.info:
            show_image_info(args.info)
            return

        # Validate arguments
        validate_args(args)

        # Process images
        if args.batch:
            process_batch(args)
        else:
            process_single_image(args)

    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except KeyboardInterrupt:
        print("\nOperation cancelled by user", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main() 