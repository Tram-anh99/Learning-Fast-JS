#!/bin/bash
echo "=== CHECKING UNUSED COMPONENTS ==="
echo ""

for component in src/components/*.vue; do
  name=$(basename "$component" .vue)
  
  # Skip if file doesn't exist
  if [ ! -f "$component" ]; then
    continue
  fi
  
  # Search for imports of this component in all files
  count=$(grep -r "import.*from.*${name}" src/ 2>/dev/null | grep -v ".history" | wc -l)
  
  if [ $count -eq 0 ]; then
    lines=$(wc -l < "$component")
    echo "❌ $name.vue - UNUSED ($lines lines)"
  fi
done

echo ""
echo "=== COMPONENT USAGE COUNT ==="
for component in src/components/*.vue; do
  name=$(basename "$component" .vue)
  if [ ! -f "$component" ]; then
    continue
  fi
  count=$(grep -r "import.*from.*${name}" src/ 2>/dev/null | grep -v ".history" | wc -l)
  lines=$(wc -l < "$component")
  printf "%-30s %3d imports, %3d lines\n" "$name.vue" "$count" "$lines"
done
