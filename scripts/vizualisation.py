from matplotlib.animation import FuncAnimation
import matplotlib.pyplot as plt
import numpy as np
import progressbar


def vizualisation(list_of_colonies, resource_matrix, rounds_number, file_name):
    bar = progressbar.ProgressBar(maxval=rounds_number,
                                  widgets=[progressbar.Bar('=', '[', ']'),
                                           ' ', progressbar.Percentage()])

    fig, ax = plt.subplots()
    im = ax.imshow(resource_matrix.matrix, alpha=1, 
                   cmap='binary')
    
    ax.axis('off')
    scats = []
    for colony in list_of_colonies:
        scats.append(
            ax.scatter([], [],
                       color=colony.color,
                       s=7, marker='o', alpha=0.9)
        )
 
    bar.start()

    def animate(frame):
        if frame % 5 == 0 or frame == rounds_number - 1:
            bar.update(frame + 1)

        resource_matrix.resupply()
        im.set_data(resource_matrix.matrix)

        for scat, colony in zip(scats, list_of_colonies):

            if colony.cells_number:
                scat.set_offsets(colony.list_of_cells_coordinates[:, [1, 0]])
            else:
                scat.set_offsets(np.empty((0, 2)))
                continue

            colony.eat(resource_matrix)

    anim = FuncAnimation(fig, animate,
                         frames=rounds_number,
                         repeat=False, blit=False)
    
    # writer = FFMpegWriter(fps=1,
    #         codec="h264",
    #         extra_args=["-preset", "veryslow","-crf","0"])

    # anim.save(__file__+".mp4", writer=writer)
    anim.save(file_name, writer='pillow')
    bar.finish()
    # plt.show()
    # plt.close()
