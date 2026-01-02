def choose_discount() -> DiscountStrategy:
    print("انتخاب نوع تخفیف:")
    print("1) بدون تخفیف")
    print("2) تخفیف درصدی")
    print("3) تخفیف مبلغ ثابت")
    print("4) تخفیف شرطی (آستانه -> درصد)")
    choice = input("شماره را وارد کنید: ").strip()
    if choice == "1":
        return NoDiscount()
    elif choice == "2":
        p = float(input("درصد را وارد کنید (مثال: 10 برای 10%): ").strip())
        return PercentageDiscount(percent=p)
    elif choice == "3":
        a = float(input("مبلغ ثابت را وارد کنید: ").strip())
        return FixedAmountDiscount(amount=a)
    elif choice == "4":
        th = float(input("آستانه (حداقل مجموع برای اعمال تخفیف) را وارد کنید: ").strip())
        p = float(input("درصد تخفیف را وارد کنید: ").strip())
        return ThresholdPercentageDiscount(threshold=th, percent=p)
    else:
        print("انتخاب نامعتبر، بدون تخفیف اعمال می‌شود.")
        return NoDiscount()


def main_loop():
    inv = Inventory()
    seed_inventory(inv)
    user = User(name="مشتری")

    while True:
        print("\n--- منوی اصلی ---")
        print("1) نمایش محصولات")
        print("2) جستجو بر اساس نام یا دسته")
        print("3) اضافه کردن به سبد")
        print("4) نمایش سبد")
        print("5) تغییر تعداد / حذف از سبد")
        print("6) تسویه حساب (checkout)")
        print("7) نمایش سفارش‌ها")
        print("8) خروج")
        choice = input("یک گزینه را انتخاب کنید: ").strip()

        try:
            if choice == "1":
                print_products(inv.list_products())

            elif choice == "2":
                k = input("کلمه برای جستجو وارد کنید: ").strip()
                results = inv.search_by_name_or_category(k)
                print_products(results)

            elif choice == "3":
                pid = input("آی‌دی محصول را وارد کنید (مثال P001): ").strip()
                p = inv.find_by_id(pid)
                if not p:
                    print("محصولی با این آی‌دی یافت نشد")
                    continue
                qty = int(input("تعداد را وارد کنید: ").strip())
                user.cart.add_item(p, qty)
                print("به سبد اضافه شد")

            elif choice == "4":
                print_cart(user.cart)

            elif choice == "5":
                print_cart(user.cart)
                pid = input("آی‌دی محصول برای تغییر/حذف وارد کنید: ").strip()
                if pid not in user.cart.items:
                    print("آن محصول در سبد نیست")
                    continue
                qty = int(input("تعداد جدید را وارد کنید (0 برای حذف): ").strip())
                user.cart.update_quantity(pid, qty)
                print("به‌روزرسانی شد")

            elif choice == "6":
                print_cart(user.cart)
                if user.cart.is_empty():
                    print("سبد خالی است؛ امکان تسویه نیست")
                    continue
                ds = choose_discount()
                total_before = user.cart.calculate_total()
                discount_amount = ds.apply(total_before)
                discount_amount = min(discount_amount, total_before)
                print(f"جمع قبل از تخفیف: {total_before:,.0f}")
                print(f"مقدار تخفیف: {discount_amount:,.0f}")
                print(f"مبلغ نهایی: {total_before - discount_amount:,.0f}")

                confirm = input("تأیید ثبت سفارش؟ (y/n): ").strip().lower()
                if confirm == 'y':
                    order = user.place_order(ds)
                    print(f"سفارش ثبت شد. شماره سفارش: {order.id}")
                else:
                    print("سفارش کنسل شد")

            elif choice == "7":
                orders = user.list_orders()
                if not orders:
                    print("سفارشی ثبت نشده")
                else:
                    for o in orders:
                        print("-" * 40)