longest_video() {
    local dir="${1:-.}"  # Default to current directory if none given
    local longest_duration=0
    local longest_file=""

    # Loop through video files (you can adjust pattern if needed)
    for f in "$dir"/*.mp4; do
        if [[ -f "$f" ]]; then
            # Get duration in seconds
            duration=$(ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 "$f")
            duration=${duration%.*}  # Remove fractional part

            if [[ "$duration" -gt "$longest_duration" ]]; then
                longest_duration=$duration
                longest_file="$f"
            fi
        fi
    done

    echo "📽️ Longest video: $longest_file"
    echo "⏱️ Duration: ${longest_duration}s"
}