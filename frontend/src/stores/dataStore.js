import { defineStore } from 'pinia'
import { ref, computed, watch } from 'vue'
import dayjs from 'dayjs'
import {
  fetchGoiList,
  fetchSaleList,
  fetchPtChamSocList,
  fetchCsNhapList,
  fetchGoiDetail,
  fetchAllRecords,
  createRecord,
  updateRecord,
  deleteRecord,
} from '../services/api'

export const useDataStore = defineStore('data', () => {
  const goiOptions = ref([])
  const saleOptions = ref([])
  const ptChamSocOptions = ref([])
  const csNhapOptions = ref([])
  const records = ref([])
  const savedRecords = ref([])

  const form = ref({
    stt: null,
    clb: null,
    ngay: null,
    thang: null,
    nam: null,
    soBN: null,
    maKH: '',
    hoTenKH: '',
    ngaySinh: null,
    sdt: '',
    maGoi: null,
    sale: null,
    ptChamSoc: null,
    csNhap: null,
    ptGym: 0,
    pttl: 0,
    daily: 0,
    boi: 0,
    ptTang: 0,
    buoiPtCoDinh: 0,
    soThang: 0,
    congThangBL: 0,
    congThangTang: 0,
    congNgayTang: 0,
    khungGioTap: '',
    chuyenNhuong: '',
    soHD: '',
    ngayBatDau: null,
    tongNgayDaDi: 0,
    quaTang: '',
    mucUuDai: 0,
    bnDatCoc: '',
    tenGoiNangCap: '',
    soTienKHNangCap: '',
    khDaDatCoc: '',
    tongDatCocNangCap: '',
    conPhaiThuKH: '',
    phanTramSaleDT: 1,
    datCoc: '',
    ttPhanThieu: '',
    dongFull: '',
    phiPos: '',
    doanhThu: '',
    hinhThucTT: '',
    daNhanTM: '',
    ckChung: '',
    tongTienCKChung: '',
    trangThai: '',
    tongGoiTap: '',
    loai: '',
    luot: '',
    nguon: '',
    tinhTrang: '',
    daNhapTimeSoft: '',
    ghiChu: '',
    daKichHoat: false,
    tongHopDayShowGX: '',
    thangHoanThienHD: '',
  })

  const selectedGoi = ref(null)

  function resetForm() {
    form.value = {
      stt: null,
      clb: null,
      ngay: null,
      thang: null,
      nam: null,
      soBN: null,
      maKH: '',
      hoTenKH: '',
      ngaySinh: null,
      sdt: '',
      maGoi: null,
      sale: null,
      ptChamSoc: null,
      csNhap: null,
      ptGym: 0,
      pttl: 0,
      daily: 0,
      boi: 0,
      ptTang: 0,
      buoiPtCoDinh: 0,
      soThang: 0,
      congThangBL: 0,
      congThangTang: 0,
      congNgayTang: 0,
      khungGioTap: '',
      chuyenNhuong: '',
      soHD: '',
      ngayBatDau: null,
      tongNgayDaDi: 0,
      quaTang: '',
      mucUuDai: 0,
      bnDatCoc: '',
      tenGoiNangCap: '',
      soTienKHNangCap: '',
      khDaDatCoc: '',
      tongDatCocNangCap: '',
      conPhaiThuKH: '',
      phanTramSaleDT: 1,
      datCoc: '',
      ttPhanThieu: '',
      dongFull: '',
      phiPos: '',
      doanhThu: '',
      hinhThucTT: '',
      daNhanTM: '',
      ckChung: '',
      tongTienCKChung: '',
      trangThai: '',
      tongGoiTap: '',
      loai: '',
      luot: '',
      nguon: '',
      tinhTrang: '',
      daNhapTimeSoft: '',
      ghiChu: '',
      daKichHoat: false,
      tongHopDayShowGX: '',
      thangHoanThienHD: '',
    }
    selectedGoi.value = null
  }

  const ngayThangNam = computed(() => {
    const { ngay, thang, nam } = form.value
    if (ngay && thang && nam) {
      return `${String(ngay).padStart(2, '0')}/${String(thang).padStart(2, '0')}/${nam}`
    }
    return ''
  })

  const quyenSo = computed(() => {
    const bn = form.value.soBN
    if (bn === null || bn === undefined || bn === '') return null
    const num = Number(bn)
    if (isNaN(num)) return 0
    return Math.ceil(num / 50)
  })

  const loaiThe1 = computed(() => {
    return selectedGoi.value?.maLoaiTheTarget || ''
  })

  const loaiThe2 = computed(() => {
    return selectedGoi.value?.maLoaiTheLocPT || ''
  })

  const phanBo1 = computed(() => {
    return selectedGoi.value?.phanBo || ''
  })

  const soThangBuoi = computed(() => {
    return selectedGoi.value?.thoiGian || ''
  })

  const donGiaNiemYet = computed(() => {
    return selectedGoi.value?.giaNiemYet || 0
  })

  const tongSS = computed(() => {
    const f = form.value
    return (f.ptGym || 0) + (f.pttl || 0) + (f.daily || 0) + (f.boi || 0) + (f.ptTang || 0)
  })

  const tongSoThang = computed(() => {
    const f = form.value
    return (f.soThang || 0) + (f.congThangBL || 0) + (f.congThangTang || 0)
  })

  const goiTap = computed(() => {
    const f = form.value
    const parts = [f.maGoi]
    if (f.ptGym) parts.push(String(f.ptGym))
    if (f.pttl) parts.push(String(f.pttl))
    if (f.daily) parts.push(String(f.daily))
    if (f.ptTang) parts.push(String(f.ptTang))
    return parts.join(' ')
  })

  const ngayKetThuc = computed(() => {
    if (!form.value.ngayBatDau || !tongSoThang.value) return null
    return dayjs(form.value.ngayBatDau).add(tongSoThang.value, 'month').toDate()
  })

  const tongSoNgay = computed(() => {
    if (!form.value.ngayBatDau || !ngayKetThuc.value) return 0
    return dayjs(ngayKetThuc.value).diff(dayjs(form.value.ngayBatDau), 'day')
  })

  const tongSoNgayConLai = computed(() => {
    if (!tongSoNgay.value) return 0
    return tongSoNgay.value - (form.value.tongNgayDaDi || 0)
  })

  const tinhTrangText = computed(() => {
    if (!ngayKetThuc.value) return ''
    const today = dayjs()
    const end = dayjs(ngayKetThuc.value)
    const diff = end.diff(today, 'day')
    if (diff > 0) return `Còn ${diff} ngày`
    if (diff === 0) return 'Hết hạn hôm nay'
    return `Đã hết hạn ${Math.abs(diff)} ngày rồi`
  })

  const tongTienBaoLuu = computed(() => {
    return (donGiaNiemYet.value || 0) * (form.value.congThangBL || 0)
  })

  const tongTienBuoiDay = computed(() => {
    const f = form.value
    const totalBuoi = (f.ptGym || 0) + (f.pttl || 0) + (f.daily || 0) + (f.ptTang || 0)
    return (donGiaNiemYet.value || 0) * totalBuoi
  })

  const tongTien = computed(() => {
    return Math.max(donGiaNiemYet.value || 0, tongTienBaoLuu.value, tongTienBuoiDay.value)
  })

  const soTienKHGiam = computed(() => {
    return tongTien.value * ((form.value.mucUuDai || 0) / 100)
  })

  const tong = computed(() => {
    return tongTien.value - soTienKHGiam.value
  })

  const soTienDVPhaiThu = computed(() => {
    return tong.value * ((form.value.phanTramSaleDT || 0) / 100)
  })

  function setSelectedGoi(maGoi) {
    if (!maGoi) {
      selectedGoi.value = null
      return
    }
    selectedGoi.value = goiOptions.value.find(g => g.maGoi === maGoi) || null
  }

  function setFormFromRecord(record) {
    form.value = { ...record }
    if (record.maGoi) {
      setSelectedGoi(record.maGoi)
    }
  }

  function fixNumber(val) {
    if (val === null || val === undefined || val === '') return 0
    const num = Number(val)
    return isNaN(num) ? 0 : num
  }

  function mapRecordToRow(record) {
    const d = record
    const startDate = d.ngayBatDau ? dayjs(d.ngayBatDau).format('YYYY-MM-DD') : ''
    const endDate = d.ngayKetThuc ? dayjs(d.ngayKetThuc).format('YYYY-MM-DD') : ''

    return [
      d.stt || '',
      d.clb || '',
      d.ngay || '',
      d.thang || '',
      d.nam || '',
      d.ngayThangNam || '',
      d.quyenSo ?? '',
      d.soBN ?? '',
      d.maKH || '',
      d.hoTenKH || '',
      d.ngaySinh || '',
      d.sdt || '',
      d.maGoi || '',
      d.sale || '',
      d.ptChamSoc || '',
      d.phanBo1 || '',
      d.loaiThe1 || '',
      d.loaiThe2 || '',
      d.phanBo2 || '',
      d.csNhap || '',
      d.tongSS ?? 0,
      d.ptGym ?? 0,
      d.pttl ?? 0,
      d.daily ?? 0,
      d.boi ?? 0,
      d.ptTang ?? 0,
      d.buoiPtCoDinh ?? 0,
      d.soThang ?? 0,
      d.tongSoThang ?? 0,
      d.congThangBL ?? 0,
      d.congThangTang ?? 0,
      d.congNgayTang ?? 0,
      d.goiTap || '',
      d.khungGioTap || '',
      d.chuyenNhuong || '',
      d.soHD || '',
      d.soThangBuoi || '',
      startDate,
      '',
      '',
      '',
      '',
      '',
      '',
      endDate,
      d.tinhTrang || '',
      d.tongSoNgay ?? 0,
      d.tongNgayDaDi ?? 0,
      '',
      d.tongSoNgayConLai ?? 0,
      d.quaTang || '',
      d.donGiaNiemYet ?? 0,
      d.tongTienBaoLuu ?? 0,
      d.tongTienBuoiDay ?? 0,
      '',
      '',
      d.tongTien ?? 0,
      d.mucUuDai ?? 0,
      d.soTienKHGiam ?? 0,
      d.tong ?? 0,
      d.soTienDVPhaiThu ?? 0,
      d.bnDatCoc || '',
      d.tenGoiNangCap || '',
      d.soTienKHNangCap || '',
      d.khDaDatCoc || '',
      d.tongDatCocNangCap || '',
      d.conPhaiThuKH || '',
      d.phanTramSaleDT ?? 0,
      d.datCoc || '',
      d.ttPhanThieu || '',
      d.dongFull || '',
      d.phiPos || '',
      d.doanhThu || '',
      d.hinhThucTT || '',
      d.daNhanTM || '',
      d.ckChung || '',
      d.tongTienCKChung || '',
      d.trangThai || '',
      d.tongGoiTap || '',
      d.loai || '',
      d.luot || '',
      d.nguon || '',
      d.tinhTrang || '',
      d.daNhapTimeSoft || '',
      d.ghiChu || '',
      d.daKichHoat || '',
      d.tongHopDayShowGX || '',
      d.thangHoanThienHD || '',
    ]
  }

  async function loadGoiOptions() {
    try {
      const res = await fetchGoiList()
      goiOptions.value = res.data || []
    } catch (e) {
      console.error('Failed to load goi options:', e)
    }
  }

  async function loadDropdowns() {
    try {
      const [goiRes, saleRes, ptRes, csRes] = await Promise.all([
        fetchGoiList(),
        fetchSaleList(),
        fetchPtChamSocList(),
        fetchCsNhapList(),
      ])
      goiOptions.value = goiRes.data || []
      saleOptions.value = saleRes.data || []
      ptChamSocOptions.value = ptRes.data || []
      csNhapOptions.value = csRes.data || []
    } catch (e) {
      console.error('Failed to load dropdowns:', e)
    }
  }

  async function loadRecords() {
    try {
      const res = await fetchAllRecords()
      savedRecords.value = res.data || []
    } catch (e) {
      console.error('Failed to load records:', e)
    }
  }

  async function saveRecord(formData) {
    const data = {
      ...formData,
      ngayThangNam: ngayThangNam.value,
      quyenSo: quyenSo.value,
      loaiThe1: loaiThe1.value,
      loaiThe2: loaiThe2.value,
      phanBo1: phanBo1.value,
      soThangBuoi: soThangBuoi.value,
      donGiaNiemYet: donGiaNiemYet.value,
      tongSS: tongSS.value,
      tongSoThang: tongSoThang.value,
      goiTap: goiTap.value,
      ngayKetThuc: ngayKetThuc.value,
      tongSoNgay: tongSoNgay.value,
      tongSoNgayConLai: tongSoNgayConLai.value,
      tinhTrang: tinhTrangText.value,
      tongTienBaoLuu: tongTienBaoLuu.value,
      tongTienBuoiDay: tongTienBuoiDay.value,
      tongTien: tongTien.value,
      soTienKHGiam: soTienKHGiam.value,
      tong: tong.value,
      soTienDVPhaiThu: soTienDVPhaiThu.value,
    }
    try {
      const res = await createRecord(data)
      return res.data
    } catch (e) {
      console.error('Failed to save record:', e)
      throw e
    }
  }

  return {
    goiOptions,
    saleOptions,
    ptChamSocOptions,
    csNhapOptions,
    records,
    savedRecords,
    form,
    selectedGoi,
    ngayThangNam,
    quyenSo,
    loaiThe1,
    loaiThe2,
    phanBo1,
    soThangBuoi,
    donGiaNiemYet,
    tongSS,
    tongSoThang,
    goiTap,
    ngayKetThuc,
    tongSoNgay,
    tongSoNgayConLai,
    tinhTrangText,
    tongTienBaoLuu,
    tongTienBuoiDay,
    tongTien,
    soTienKHGiam,
    tong,
    soTienDVPhaiThu,
    resetForm,
    setSelectedGoi,
    setFormFromRecord,
    loadDropdowns,
    loadGoiOptions,
    loadRecords,
    saveRecord,
    deleteRecord,
  }
})
