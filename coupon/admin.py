from django.contrib import admin
from coupon.models import Coupon,CouponItem
from django.utils import timezone


@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = (
        'coupon_code',
        'coupon_name',
        'discount_display',
        'min_purchase_amount_display',
        'is_active',
        'start_date',
        'end_date',
        'status_badge',
    )

    # Sağ tərəfdəki filtr paneli
    list_filter = (
        'is_active',
        'start_date',
        'end_date',
        'created_at',
    )

    # Axtarış paneli (Kupon kodu və adına görə)
    search_fields = (
        'coupon_code',
        'coupon_name',
    )

    # Tarixə görə dinamik hiyerarxik filter
    date_hierarchy = 'created_at'

    # Form daxilində sahələrin qruplaşdırılması (Tərtibatı daha səliqəli edir)
    fieldsets = (
        (
            'Əsas Məlumatlar',
            {'fields': ('coupon_name', 'coupon_code', 'is_active')},
        ),
        (
            'Güzəşt və Məbləğ Şərtləri',
            {
                'fields': ('discount', 'min_purchase_amount'),
                'description': (
                    'Əgər minimum səbət məbləği tələb olunmursa,'
                    ' "min_purchase_amount" sahəsini boş saxlayın.'
                ),
            },
        ),
        ('Keçərlilik Müddəti', {'fields': ('start_date', 'end_date')}),
        (
            'Sistem Tarixləri (Oxunabilir)',
            {
                'fields': ('created_at', 'updated_at'),
                'classes': ('collapse',),  # Bu hissəni gizlədilib-açılan edir
            },
        ),
    )

    # BaseDatabaseModel-dəki avtomatik doldurulan alanları yalnız oxunabilir edirik
    readonly_fields = ('created_at', 'updated_at')

    # -------------------------------------------------------------------
    # Xüsusi Görünüş və Metodlar (Custom Display Functions)
    # -------------------------------------------------------------------

    @admin.display(description='Güzəşt (%)')
    def discount_display(self, obj):
        return f'%{obj.discount}'

    @admin.display(description='Min. Səbət Məbləği')
    def min_purchase_amount_display(self, obj):
        if obj.min_purchase_amount is not None:
            return f'{obj.min_purchase_amount} AZN'
        return 'Şərt Yoxdur'

    @admin.display(description='Müddət Statusu')
    def status_badge(self, obj):
        """Kuponun vaxtının keçib-keçmədiyini vizual olaraq göstərir."""
        now = timezone.now()

        if not obj.is_active:
            return '❌ Deaktiv'
        if obj.start_date > now:
            return '⏳ Gözləmədə (Başlamayıb)'
        if obj.end_date < now:
            return '⚠️ Vaxtı Bitib'
        return '✅ Aktivdir'



@admin.register(CouponItem)
class CouponItemAdmin(admin.ModelAdmin):
  # Cədvəldə görünəcək sütunlar
  list_display = (
      'id',
      'coupon',
      'user',
      'used_at',
      'created_at',
  )

  # Sağ tərəfdəki filtr paneli
  list_filter = (
      'used_at',
      'created_at',
  )

  # Axtarış sahələri (Kupon kodu, kupon adı və ya istifadəçi adına görə)
  # Qeyd: Users modelinizin içindəki sahələrdən asılı olaraq 'user__username' və ya 'user__email' işlədə bilərsiniz.
  search_fields = (
      'coupon__coupon_code',
      'coupon__coupon_name',
      'user__username',  # Əgər istifadəçi modelinizdə 'username' varsa
  )

  # Tarixə görə dinamik hiyerarxik filter
  date_hierarchy = 'used_at'

  # Form daxilində sahələrin nizamlanması
  fieldsets = (
      (
          'İstifadə Məlumatları',
          {
              'fields': (
                  'coupon',
                  'user',
                  'used_at',
              )
          },
      ),
      (
          'Sistem Tarixləri',
          {
              'fields': ('created_at', 'updated_at'),
              'classes': ('collapse',),
          },
      ),
  )

  # Avtomatik yaradılan sahələri yalnız oxunabilir edirik
  readonly_fields = ('created_at', 'updated_at')