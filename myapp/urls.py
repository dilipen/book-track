# from django.contrib import admin
# from django.conf import settings
from django.conf.urls import url

from .views.user import UserCreateList, UserRetriveUpdateDelete

urlpatterns = []

urlpatterns.append(url(r'^users$', UserCreateList.as_view()))
urlpatterns.append(url(r'^users/(?P<user>\d)$', UserRetriveUpdateDelete.as_view()))  # noqa: E501


from .views.publisher_book import PublisherBookCreateList, PublisherBookRetriveUpdateDelete

urlpatterns.append(url(r'^publisher/books$', PublisherBookCreateList.as_view()))
urlpatterns.append(url(r'^publisher/books/(?P<book>\d)$', PublisherBookRetriveUpdateDelete.as_view()))

from .views.publisher_paper_book_order import PublisherPaperBookOrderCreateList, PublisherPaperBookOrderRetriveUpdateDelete, BookDispatch, BookHandOverToTransport, PublisherPaperBookOrderHandOverList

urlpatterns.append(url(r'^publisher/paper-book-orders$', PublisherPaperBookOrderCreateList.as_view()))
urlpatterns.append(url(r'^publisher/paper-book-orders/(?P<paper_book_order>\d)$', PublisherPaperBookOrderRetriveUpdateDelete.as_view()))
urlpatterns.append(url(r'^publisher/paper-book-orders/(?P<paper_book_order>\d)/dispatch$', BookDispatch.as_view()))
urlpatterns.append(url(r'^publisher/paper-book-orders/(?P<paper_book_order>\d)/handover-to-transport$', BookHandOverToTransport.as_view()))

urlpatterns.append(url(r'^publisher/paper-book-orders/handover-list$', PublisherPaperBookOrderHandOverList.as_view()))



from .views.buyer_cart import BuyerCartCreateList, BuyerCartRetriveUpdateDelete, CartSubmit

urlpatterns.append(url(r'^buyer/carts$', BuyerCartCreateList.as_view()))
urlpatterns.append(url(r'^buyer/carts/(?P<cart>\d)$', BuyerCartRetriveUpdateDelete.as_view()))

urlpatterns.append(url(r'^buyer/carts-submit/(?P<user_address>\d)$', CartSubmit.as_view()))

from .views.buyer_order import BuyerOrderCreateList, BuyerOrderRetriveUpdateDelete

urlpatterns.append(url(r'^buyer/orders$', BuyerOrderCreateList.as_view()))
urlpatterns.append(url(r'^buyer/orders/(?P<order>\d)$', BuyerOrderRetriveUpdateDelete.as_view()))

from .views.buyer_order_detail import BuyerOrderDetailCreateList, BuyerOrderDetailRetriveUpdateDelete

urlpatterns.append(url(r'^buyer/orders/(?P<order>\d)/order-details$', BuyerOrderDetailCreateList.as_view()))
urlpatterns.append(url(r'^buyer/orders/(?P<order>\d)/order-details/(?P<order_detail>\d)$', BuyerOrderDetailRetriveUpdateDelete.as_view()))


from .views.transporter_paper_book_order import TransporterPaperBookOrderCreateList, TransporterPaperBookOrderRetriveUpdateDelete, TransporterPaperBookOrderDeliveredList

urlpatterns.append(url(r'^transporter/paper-book-orders$', TransporterPaperBookOrderCreateList.as_view()))
urlpatterns.append(url(r'^transporter/paper-book-orders/(?P<paper_book_order>\d)$', TransporterPaperBookOrderRetriveUpdateDelete.as_view()))

urlpatterns.append(url(r'^transporter/paper-book-orders/delivered-list$', TransporterPaperBookOrderDeliveredList.as_view()))

from .views.transporter_paper_book_order_track import TransporterPaperBookOrderTrackCreateList, TransporterPaperBookOrderTrackRetriveUpdateDelete

urlpatterns.append(url(r'^transporter/paper-book-orders/(?P<paper_book_order>\d)/paper-book-order-tracks$', TransporterPaperBookOrderTrackCreateList.as_view()))
urlpatterns.append(url(r'^transporter/paper-book-orders/(?P<paper_book_order>\d)/paper-book-order-tracks/(?P<paper_book_order_track>\d)$', TransporterPaperBookOrderTrackRetriveUpdateDelete.as_view()))

from .views.buyer_user_address import BuyerUserAddressCreateList, BuyerUserAddressRetriveUpdateDelete

urlpatterns.append(url(r'^buyer/user-address$', BuyerUserAddressCreateList.as_view()))
urlpatterns.append(url(r'^buyer/user-address/(?P<user_address>\d)$', BuyerUserAddressRetriveUpdateDelete.as_view()))

from .views.buyer_show_book import BuyerShowBookCreateList

urlpatterns.append(url(r'^buyer/show-books$', BuyerShowBookCreateList.as_view()))