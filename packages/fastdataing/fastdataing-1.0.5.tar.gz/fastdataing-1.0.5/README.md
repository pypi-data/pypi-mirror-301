### Common fast data processing methods

> A collection of frequently employed functions!

#### Smooth

- smooth_MIS(x,y,factor=300): 
  - smooth data
- smooth_SF(x,y,factors=[5,3]): 
  - smooth data

### files processing

- get_files(directory, suffix): 
  - Read files with the same suffix in the folder and save them as a list

### plot figs

- add_fig(figsize=(10,8)): 
  - add a canvas, return ax
- plot_fig(ax,x,y,label=False,linewidth=1,
  	factors=False,color="r",savefig="temp.png",
  	xlabel=False,ylabel=False,fontweight="bold",alpha=1.0,
  	dpi=300,transparent=True,fontsize=26):
  - plot fig

### Figure Processing

- fig2ico(png_file,ico_file=False):
  - convert png to ico file
- fig2binary(fig_file, binary_file=False, threshold=128):
  - convert fig to binary image
- binary2dxf(binary_image_file,dxf_file=False):
  - convert binary to dxf format

### ...