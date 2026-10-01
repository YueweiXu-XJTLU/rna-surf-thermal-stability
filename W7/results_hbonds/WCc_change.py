import matplotlib.pyplot as plt

def read_init_file(file_path):
    """Read initial pairing.out file (no # Frame line)"""
    frame_data = {}
    with open(file_path, 'r') as f:
        for line in f:
            parts = line.strip().split()
            if len(parts) != 3:
                continue
            bp1, bp2, bp_type = parts
            bp_pair = tuple(sorted((bp1, bp2)))
            frame_data[bp_pair] = bp_type
    return {0: frame_data}


def read_track_file(file_path):
    """Read 0–500 pairing.out file"""
    frames = {}
    current_frame = None
    with open(file_path, 'r') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            if line.startswith("# Frame"):
                current_frame = int(line.split()[2])
                frames[current_frame] = {}
                continue
            parts = line.split()
            if len(parts) != 3:
                continue
            bp1, bp2, bp_type = parts
            bp_pair = tuple(sorted((bp1, bp2)))
            if current_frame is not None:
                frames[current_frame][bp_pair] = bp_type
    return frames


def analyze_wcc(init_frames, track_frames, output_txt):
    frame_keys = sorted(track_frames.keys())
    prev_frame_data = init_frames[0]

    # Count WCc in initial file
    init_wcc_count = sum(1 for t in init_frames[0].values() if t == "WCc")

    frame_list = []
    wcc_count_list = []
    wcc_to_other_list = []
    wcc_to_no_pair_list = []
    new_wcc_list = []

    with open(output_txt, 'w') as out:
        # Add initial WCc count at the top
        out.write(f"Initial_WCc_count: {init_wcc_count}\n\n")

        for frame in frame_keys:
            current_data = track_frames[frame]

            # WCc count in current frame
            wcc_count = sum(1 for t in current_data.values() if t == "WCc")

            # WCc → other type
            wcc_to_other = sum(
                1 for bp, t in prev_frame_data.items()
                if t == "WCc" and bp in current_data and current_data[bp] != "WCc" and current_data[bp] != "No_Pair"
            )

            # WCc → No_Pair
            wcc_to_no_pair = sum(
                1 for bp, t in prev_frame_data.items()
                if t == "WCc" and (bp not in current_data or current_data[bp] == "No_Pair")
            )

            # New WCc generated
            new_wcc = sum(
                1 for bp, t in current_data.items()
                if t == "WCc" and (bp not in prev_frame_data or prev_frame_data[bp] != "WCc")
            )

            frame_list.append(frame)
            wcc_count_list.append(wcc_count)
            wcc_to_other_list.append(wcc_to_other)
            wcc_to_no_pair_list.append(wcc_to_no_pair)
            new_wcc_list.append(new_wcc)

            out.write(f"# Frame {frame}\n")
            out.write(f"WCc_count: {wcc_count}\n")
            out.write(f"WCc_to_other: {wcc_to_other}\n")
            out.write(f"WCc_to_No_Pair: {wcc_to_no_pair}\n")
            out.write(f"New_WCc: {new_wcc}\n\n")

            prev_frame_data = current_data

        # Summary
        diffs = [abs(wcc_count_list[i] - wcc_count_list[i - 1]) for i in range(1, len(wcc_count_list))]
        if diffs:
            max_diff = max(diffs)
            max_diff_frame = frame_list[diffs.index(max_diff) + 1]
            out.write("==== Summary ====\n")
            out.write(f"Most significant WCc change frame: Frame {max_diff_frame}, Change: {max_diff}\n")
        else:
            out.write("==== Summary ====\n")
            out.write("Not enough frames to calculate change\n")

    return frame_list, wcc_count_list


def plot_wcc_stats(frame_list, wcc_count_list):
    """Plot WCc count trend"""
    plt.figure(figsize=(10, 6))

    plt.plot(frame_list, wcc_count_list, label="WCc_count", marker='o')

    plt.xlabel("Frame")
    plt.ylabel("WCc Count")
    plt.title("WCc Count Trend (0-500 frames)")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig("wcc_count_plot.png", dpi=300)
    plt.show()


if __name__ == "__main__":
    init_file = "basepair_annotate_pairing_300k.csv"
    track_file = "basepair_annotate_pairing_300k.csv"
    output_txt = "wcc_changes.txt"

    init_frames = read_init_file(init_file)
    track_frames = read_track_file(track_file)

    frame_list, wcc_count_list = analyze_wcc(init_frames, track_frames, output_txt)

    print(f"Analysis complete. Results saved to {output_txt}")

    plot_wcc_stats(frame_list, wcc_count_list)
