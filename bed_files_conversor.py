def bed_files_conversor(run):

    import os
    import pandas

    path = "C:/Users/Usuario/Desktop/PRUEBA_0" + str(run)
    all_files = (os.listdir(path))
    bed_files = []

    for i in all_files:
        if i.endswith("target_bed_read_cov_report.bed"):
            bed_files.append(i)

    for i in bed_files:
        bed_path = path + "/" + i
        xlsx_path = path + "/" + i[0:8]
        bed_file = pandas.read_csv(bed_path, sep = "\t")
        bed_file.to_excel(xlsx_path + ".xlsx", i[0:8], index = False)
        os.remove(bed_path)