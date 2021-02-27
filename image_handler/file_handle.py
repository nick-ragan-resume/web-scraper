def UploadAction(event=None):
    filename = filedialog.askopenfilename()
    print('Selected:', filename)