import { ref, shallowRef } from 'vue';
import L from 'leaflet';

export function useMapLogic() {
  const map = shallowRef(null);
  const mapContainer = ref(null);
  const lopSauBenh = shallowRef(L.layerGroup());
  const cheDoXem = ref('hanh_chinh');

  const initMap = (coordinates = [10.765, 106.660], zoom = 13) => {
    if (!mapContainer.value) return;

    map.value = L.map(mapContainer.value, { zoomControl: false }).setView(coordinates, zoom);
    L.control.zoom({ position: 'bottomright' }).addTo(map.value);

    // Nền bản đồ sáng (CartoDB Positron)
    L.tileLayer('https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png', {
      attribution: '© CartoDB'
    }).addTo(map.value);

    lopSauBenh.value.addTo(map.value);
  };

  const vẽMarkerVùng = (danhSachVung) => {
    danhSachVung.forEach(vung => {
      const color = vung.trangThai === 'active' ? '#1b4332' : 
                    (vung.trangThai === 'warning' ? '#f59e0b' : '#ef4444');
      L.circleMarker(vung.toaDo, {
        radius: 8,
        fillColor: color,
        color: '#fff',
        weight: 2,
        fillOpacity: 1
      }).bindPopup(`<b>${vung.ten}</b><br>Chủ hộ: ${vung.chu}`).addTo(map.value);
    });
  };

  const batCheDoSauBenh = (diemNongSauBenh) => {
    cheDoXem.value = 'sau_benh';
    lopSauBenh.value.clearLayers();

    diemNongSauBenh.forEach(coord => {
      L.circle(coord, {
        color: 'red',
        fillColor: '#f03',
        fillOpacity: 0.4,
        radius: 300
      }).addTo(lopSauBenh.value);
    });
  };

  const batCheDoHanhChinh = () => {
    cheDoXem.value = 'hanh_chinh';
    lopSauBenh.value.clearLayers();
  };

  return {
    map,
    mapContainer,
    lopSauBenh,
    cheDoXem,
    initMap,
    vẽMarkerVùng,
    batCheDoSauBenh,
    batCheDoHanhChinh
  };
}
