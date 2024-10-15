import logging
import magpack.structures
import vector
import image


def plot_skyrmion():
    """Plots a skyrmion using matplotlib and pyvtk."""
    v_field = magpack.structures.skyrmion(20, 20, 1)
    v_field = magpack.structures.stack_config(v_field, 10, -1)
    vector.plot_vector_field(v_field)
    image.plot_3d(v_field)


def plot_meron():
    """Plots a meron-antimeron pair using matplotlib and pyvtk."""
    v_field = magpack.structures.meron_pair(20, 40)
    v_field = magpack.structures.stack_config(v_field, 10, -1)

    vector.plot_vector_field(v_field)
    image.plot_3d(v_field, axial=True)


if __name__ == "__main__":
    logging.getLogger().setLevel(logging.INFO)
    print("Choose a structure to plot: ")
    print("1. Skyrmion")
    print("2. Meron")

    choice = input()

    if choice == "1":
        plot_skyrmion()
    elif choice == "2":
        plot_meron()
    else:
        print("Invalid choice")
