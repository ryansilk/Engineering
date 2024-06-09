import streamlit as st

def find_best_cut(total_length, cut_lengths, buffer_length):
    num_pieces = len(cut_lengths)
    # Apply buffer to each cut length
    cut_lengths = [round(cut + buffer_length, 2) for cut in cut_lengths]
    cut_lengths.sort(reverse=True)

    # Helper function to check if a combination of cuts is valid
    def is_valid_combination(cuts, piece_length):
        return sum(cuts) <= piece_length

    # Recursive function to find the best way to cut
    def search(remaining_lengths, current_cuts, used_lengths):
        if not remaining_lengths:
            return current_cuts, used_lengths
        
        cut_length = remaining_lengths[0]
        remaining_lengths = remaining_lengths[1:]

        best_cuts = None
        min_used_lengths = float('inf')

        for i in range(len(current_cuts)):
            if is_valid_combination(current_cuts[i] + [cut_length], total_length):
                new_cuts = [cut[:] for cut in current_cuts]
                new_cuts[i].append(cut_length)
                cuts, lengths = search(remaining_lengths, new_cuts, used_lengths)
                if lengths < min_used_lengths:
                    best_cuts = cuts
                    min_used_lengths = lengths
        
        new_cuts = [cut[:] for cut in current_cuts] + [[cut_length]]
        cuts, lengths = search(remaining_lengths, new_cuts, used_lengths + 1)
        if lengths < min_used_lengths:
            best_cuts = cuts
            min_used_lengths = lengths

        return best_cuts, min_used_lengths

    best_cuts, used_lengths = search(cut_lengths, [[]], 1)
    return best_cuts, used_lengths

def main():
    st.set_page_config(page_title="Steel Cut Optimizer", layout="centered")
    st.title("Steel Cut Optimizer")

    st.sidebar.title("Instructions")
    st.sidebar.info("""
    1. Enter the total length of the master steel piece in mm.\n
    2. Enter the number of pieces you want to cut.\n
    3. Enter the length of each piece you want to cut in mm.\n
    4. Enter the buffer length in mm for each cut. This is the unusable piece due to cutting errors.\n
    5. Click the "Optimize Cuts" button to calculate the best way to cut the steel.
    """)

    st.header("Input Parameters")
    total_length = st.number_input("Enter the total length of the steel piece (mm):", min_value=0.0, format="%.2f")
    num_cuts = st.number_input("Enter the number of pieces to cut:", min_value=1, step=1)

    cut_lengths = []
    invalid_input = False
    for i in range(num_cuts):
        length = st.number_input(f"Enter the length of piece {i + 1} (mm):", min_value=0.0, format="%.2f")
        if length > total_length:
            st.error(f"Piece {i + 1} length ({length} mm) cannot be longer than the total length of the steel piece ({total_length} mm).")
            invalid_input = True
        cut_lengths.append(length)

    buffer_length = st.number_input("Enter the buffer length for each cut (mm):", min_value=0.0, format="%.2f")

    if st.button("Optimize Cuts"):
        if total_length == 0 or any(length == 0 for length in cut_lengths) or invalid_input:
            st.error("Please ensure all lengths are greater than 0 and no piece length is longer than the total length.")
        else:
            best_cuts, used_lengths = find_best_cut(total_length, cut_lengths, buffer_length)

            st.header("Results")
            st.write(f"Total Length: {total_length:.2f} mm")
            for i, cuts in enumerate(best_cuts):
                total_cuts_length = sum(cuts)
                st.write(f"Piece {i + 1}: {[round(cut, 2) for cut in cuts]} (Unused: {total_length - total_cuts_length:.2f} mm)")
            
            st.write(f"Total Pieces Used: {used_lengths}")

if __name__ == "__main__":
    main()
