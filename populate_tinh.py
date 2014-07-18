import os

def populate():
    add_tinh( name= "An Giang", region= "Nam", price_type = "2")
    add_tinh( name= "Ba Ria - Vung Tau", region= "Nam", price_type = "2")
    add_tinh( name= "Bac Giang", region= "Bac", price_type = "2")
    add_tinh( name= "Bac Kan", region= "Bac", price_type = "2")
    add_tinh( name= "Bac Lieu", region= "Nam", price_type = "2")
    add_tinh( name= "Bac Ninh", region= "Bac", price_type = "2")
    add_tinh( name= "Ben Tre", region= "Nam", price_type = "2")
    add_tinh( name= "Binh Dinh", region= "Trung", price_type = "2")
    add_tinh( name= "Binh Duong", region= "Nam", price_type = "2")
    add_tinh( name= "Binh Phuoc", region= "Nam", price_type = "2")
    add_tinh( name= "Binh Thuan", region= "Nam", price_type = "2")
    add_tinh( name= "Ca Mau", region= "Trung", price_type = "2")
    add_tinh( name= "Cao Bang", region= "Bac", price_type = "2")
    add_tinh( name= "Dak Lak", region= "Trung", price_type = "2")
    add_tinh( name= "Dak Nong", region= "Trung", price_type = "2")
    add_tinh( name= "Dien Bien", region= "Bac", price_type = "2")
    add_tinh( name= "Dong Nai", region= "Nam", price_type = "2")
    add_tinh( name= "Dong Thap", region= "Nam", price_type = "2")
    add_tinh( name= "Gia Lai", region= "Trung", price_type = "2")
    add_tinh( name= "Ha Giang", region= "Bac", price_type = "2")
    add_tinh( name= "Ha Nam", region= "Bac", price_type = "2")
    add_tinh( name= "Ha Tinh", region= "Bac", price_type = "2")
    add_tinh( name= "Hai Duong", region= "Bac", price_type = "2")
    add_tinh( name= "Hau Giang", region= "Nam", price_type = "2")
    add_tinh( name= "Hoa Binh", region= "Bac", price_type = "2")
    add_tinh( name= "Hung Yen", region= "Bac", price_type = "2")
    add_tinh( name= "Khanh Hoa", region= "Nam", price_type = "2")
    add_tinh( name= "Kien Gian", region= "Nam", price_type = "2")
    add_tinh( name= "Kon Tum", region= "Trung", price_type = "2")
    add_tinh( name= "Lai Chau", region= "Bac", price_type = "2")
    add_tinh( name= "Lam Dong", region= "Trung", price_type = "2")
    add_tinh( name= "Lang Son", region= "Bac", price_type = "2")
    add_tinh( name= "Lao Cai", region= "Bac", price_type = "2")
    add_tinh( name= "Long An", region= "Nam", price_type = "2")
    add_tinh( name= "Nam Dinh", region= "Bac", price_type = "2")
    add_tinh( name= "Nghe An", region= "Bac", price_type = "2")
    add_tinh( name= "Ninh Binh", region= "Bac", price_type = "2")
    add_tinh( name= "Ninh Thuan", region= "Trung", price_type = "2")
    add_tinh( name= "Phu Tho", region= "Bac", price_type = "2")
    add_tinh( name= "Quang Binh", region= "Bac", price_type = "2")
    add_tinh( name= "Quang Nam", region= "Trung", price_type = "2")
    add_tinh( name= "Quang Ngai", region= "Trung", price_type = "2")
    add_tinh( name= "Quang Ninh", region= "Bac", price_type = "2")
    add_tinh( name= "Quang Tri", region= "Trung", price_type = "2")
    add_tinh( name= "Soc Trang", region= "Nam", price_type = "2")
    add_tinh( name= "Son La", region= "Bac", price_type = "2")
    add_tinh( name= "Tay Ninh", region= "Nam", price_type = "2")
    add_tinh( name= "Thai Binh", region= "Bac", price_type = "2")
    add_tinh( name= "Thai Nguyen", region= "Bac", price_type = "2")
    add_tinh( name= "Thanh Hoa", region= "Bac", price_type = "2")
    add_tinh( name= "Thua Thien Hue", region= "Trung", price_type = "2")
    add_tinh( name= "Tien Giang", region= "Nam", price_type = "2")
    add_tinh( name= "Tra Vinh", region= "Nam", price_type = "2")
    add_tinh( name= "Tuyen Quang", region= "Bac", price_type = "2")
    add_tinh( name= "Vinh Long", region= "Nam", price_type = "2")
    add_tinh( name= "Vinh Phuc", region= "Bac", price_type = "2")
    add_tinh( name= "Yen Bai", region= "Bac", price_type = "2")
    add_tinh( name= "Phu Yen", region= "Trung", price_type = "2")
    add_tinh( name= "Can Tho", region= "Nam", price_type = "2")
    add_tinh( name= "Da Nang", region= "Trung", price_type = "2")
    add_tinh( name= "Hai Phong", region= "Bac", price_type = "2")
    add_tinh( name= "Ha Noi", region= "Bac", price_type = "2")
    add_tinh( name= "Sai Gon", region= "Nam", price_type = "1")

    
    #print out what we have added
    for c in Tinh.objects.all():
            print "{0}".format(str(c))


#start execution


def add_tinh(name,region,price_type):
    c = Tinh.objects.get_or_create(name=name,region=region,price_type=price_type)[0]
    return c

if __name__ =='__main__':
    print "Starting Tinh population script..."
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DLC.settings')
    from management.models import Tinh
    populate()



