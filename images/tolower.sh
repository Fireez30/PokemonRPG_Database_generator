for f in *.png; do
  mv "$f" "${f// /_}"
done
