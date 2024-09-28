import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, Product_Comment, Product_Rating
from django.contrib import messages
from django.http import HttpResponse


# Create your views here.
def home_page(request):
  
    query = request.GET.get('q') 
    products = Product.objects.all()     
    if query:
            products = products.filter(name__icontains=query)
    return render(request, 'home.html', {'product': products[::-1]})


def detail_page(request, pk):
    product = get_object_or_404(Product, id=pk)
    comments = Product_Comment.objects.filter(product=product).order_by("-id")[:3]
    pro = Product.objects.all().order_by("-created")
    products = pro[:4]
    ctx = {"product": product}
    ctx = {"product": product, "comments": comments, "products": products}
    if request.method == "POST":
        if "c_button" in request.POST:
            c_name = request.POST.get("c_name")
            c_email = request.POST.get("c_email")
            c_comment = request.POST.get("c_comment")

            comment = Product_Comment.objects.create(
                product=product, name=c_name, email=c_email, body=c_comment
            )
            comment.save()
            messages.success(request, "Comment muvofaqayatli yaratildi!")
            return redirect(f"/detail/{pk}")
        elif "Buy_product" in request.POST:
            cost = 0
            if product.new_price == 0:
                cost = product.old_price

            else:
                cost = product.new_price
            print(product.name)

            subject = request.POST.get("buy_name")
            to_email = request.POST.get("buy_email")
            body = f"<h1>{subject}- Siz {product.name}- ni ${cost} narxga  sotib oldingiz </h1>"

            # immage ketmepti manimcha buni serverga qo'ysa emailga borsa kerak
            body += f"""
                    <div class="col-md-6">
                        <img
                        class="card-img-top mb-5 mb-md-0"
                        src="{product.images.url}"
                        alt="{product.name}"
                        width="600"
                        height="700"
                        />
                    </div>
                    <div class="col-md-6">
                        <div class="small mb-1">Rating: {product.ratings}</div>
                        <h1 class="display-5 fw-bolder">{product.name}</h1>
                        <div class="fs-5 mb-5">
                        {"<span class='text-decoration-line-through'>${}</span>".format(product.old_price) if product.new_price != 0 else ""}
                        <span>${product.new_price if product.new_price != 0 else product.old_price}</span>
                        </div>
                        <p class="lead">{product.description}</p>
                        <p>Siz ushbu mahsulotni ${cost} narxda sotib oldingiz!</p>
                    </div>
                """

            smtp_server = "smtp.gmail.com"
            smtp_port = 587
            username = "sardorxonakramov2001@gmail.com"
            password = "jlvtrctoeikcsfdn"
            from_email = "Sardorning mahsuloti <sardorxonakramov2001@gmail.com>"

            msg = MIMEMultipart()
            msg["From"] = from_email
            msg["To"] = to_email
            msg["Subject"] = subject

            msg.attach(MIMEText(body, "html"))

            try:
                server = smtplib.SMTP(smtp_server, smtp_port)
                server.starttls()
                server.login(username, password)
                text = msg.as_string()
                server.sendmail(from_email, to_email, text)
                print("Email sent")
            except Exception as e:
                print(f"Failed to send email. Error: {e}")
                messages.error("ismingiz yoki epochtani xato yozdingiz")
            finally:
                server.quit()

            messages.info(
                request,
                f"{subject}- mijoz siz {product.name}ni xarid qildingiz. Raxmad! \nBarcha malumotlar emailingizni to'g'ri kiritgan bo'lsangiz sizga pochtangizga xabar keladi hammasi haqida to'liq",
            )

            return redirect(f"/detail/{pk}/")
    return render(request, "detail.html", ctx)


def filter_expensive(request):
    products = Product.objects.all()
    if products.filter(new_price=0).exists():
        sorted_products = products.order_by("-old_price")
    else:
        sorted_products = products.order_by("-new_price")
    product = sorted_products[:3]
    return render(request, "home.html", {"product": product})


def filter_cheap(request):
    products = Product.objects.all()
    if products.filter(new_price=0).exists():
        sorted_products = products.order_by("old_price")
    else:
        sorted_products = products.order_by("new_price")
    product = sorted_products[:3]
    return render(request, "home.html", {"product": product})


def filter_likes(request):
    """Reytini blanadlarni sotmoqdaman"""
    products = Product.objects.all()
    pro = products.order_by("-ratings")
    product = pro[:3]
    return render(request, "home.html", {"product": product})


def all_product(request):
    product = Product.objects.all()
    ctx = {"product": product}
    return render(request, "home.html", context=ctx)


def new_arrivals(request):
    product = Product.objects.all().order_by("-created")
    ctx = {"product": product}
    return render(request, "home.html", context=ctx)


def popular_item(request):
    products = Product.objects.all()
    pro = products.order_by("-ratings")
    product = pro[:4]
    return render(request, "home.html", {"product": product})



