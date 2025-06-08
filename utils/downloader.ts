function checkfilename(name: string, maxlength = 100) {
  const invalidregex = /[\\/:*?"<>|]/g;
  let safename = name.replace(invalidregex, "-");

  if (safename.length > maxlength) {
    safename = `${safename.slice(0, maxlength - 3)}...`;
  }

  return safename;
}

export default {
  download: async (detail: typeDetail, ifsavelyric: boolean = false) => {
    const name = encodeURIComponent(checkfilename(detail.name));
    const artist = encodeURIComponent(checkfilename(detail.artist));
    const album = encodeURIComponent(checkfilename(detail.album));
    const lyrics = detail.lyrics ? detail.lyrics : "";
    const publishtime = detail.publishtime ? detail.publishtime : "";

    let args
      = ` -s "${detail.url}"`
        + ` -f "${name} - ${artist}"`
        + ` -u "${detail.url}"`
        + ` -c "${detail.cover}"`
        + ` -l "${lyrics || ""}"`
        + ` -i ${detail.id}`
        + ` -t "${name}"`
        + ` -ar "${artist}"`
        + ` -al "${album}"`
        + ` -p "${publishtime}"`;

    if (ifsavelyric) {
      args += " -sl";
    }

    const res = (window as any).electron.invoke("download", args);
    return res;
  },

  open(path: string) {
    (window as any).electron.invoke("open", path);
  },
};
