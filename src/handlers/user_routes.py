from fastapi import APIRouter, Depends, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, JSONResponse

from src.db.models import User, UserResponse, BaseUser, UserPatch, UserAll, PostUser
from src.services.CRUD.Users_crud import create_user, get_user, update_user, update_user_partially, delete_user_f, \
    get_all_users
from src.services.auth.auth import get_current_admin, get_current_user, get_current_userr

router = APIRouter()
templates = Jinja2Templates(directory='templates')


# current_user: User = Depends(get_current_user)
@router.post("/post", response_model=PostUser)
async def create_user_endpoint(request: Request, user: PostUser):
    result = await create_user(user)
    context = {
        'request': request,
        'user': result,
    }
    return templates.TemplateResponse('user/add_user.html', context)


@router.get("/get/{username}", response_model=UserResponse)
async def read_user(username: str, current_user: UserPatch = Depends(get_current_userr)):
    print('hi read_user')
    user = await get_user(username)
    user_without_password = UserResponse(
        username=user.username,
        name=user.name,
        surname=user.surname,
        phone_number=user.phone_number,
        email=user.email
    )
    return user_without_password


@router.put("/{username}", response_model=BaseUser)
async def change_user(username: str, user: BaseUser):
    return await update_user(username, user)


@router.patch("/update/{username}", response_model=UserPatch)
async def update_user(request: Request, username: str, user: UserPatch):
    print(user)
    result = await update_user_partially(username, user)
    context = {
        'request': request,
        'results': result
    }
    return templates.TemplateResponse('user/update_user.html', context=context)


@router.delete('/delete/{username}')
async def delete_user(username: str):
    print('delete')
    return await delete_user_f(username)


@router.get('/users_all/da', response_class=HTMLResponse, name='users_all/da')
async def get_all_f_users(request: Request):
    print('hi get_all_f_users')

    users = await get_all_users()
    print(users)
    converted_users = [convert_record_to_user_patch(record) for record in users]
    print(converted_users)
    context = {
        'request': request,
        'users': converted_users
    }
    print(context)
    return templates.TemplateResponse("users_all/users_table.html", context=context)


def convert_record_to_user_patch(record):
    return UserAll(
        name=record.get('name'),
        surname=record.get('surname'),
        phone_number=record.get('phone_number'),
        email=record.get('email'),
        role=record.get('role'),
        username=record.get('username'),
    )


@router.get('/edit_form/{username}')
async def edit_user(request: Request, username: str):
    print('edit_user')
    context = {
        'request': request,
        'username': username,
    }
    return templates.TemplateResponse('user/update_user.html', context=context)


@router.get('/add_user')
async def add_user(request: Request):
    print('add_user')
    context = {
        'request': request,
    }
    return templates.TemplateResponse('user/add_user.html', context=context)

# <div class="container mt-5">
#     <h1>User List</h1>
#     <table class="table">
#         <thead>
#             <tr>
#                 <th>Name</th>
#                 <th>Surname</th>
#                 <th>Phone Number</th>
#                 <th>Email</th>
#                 <th>Role</th>
#             </tr>
#         </thead>
#         <tbody id="userTableBody">
#             {% for user in users %}
#                 <tr>
#                     <td>{{ user.name }}</td>
#                     <td>{{ user.surname }}</td>
#                     <td>{{ user.phone_number }}</td>
#                     <td>{{ user.email }}</td>
#                     <td>{{ user.role }}</td>
#                 </tr>
#             {% endfor %}
#         </tbody>
#     </table>
# </div>


   # <script>
   #      async function getUsers() {
   #          // Читаем токен из cookies
   #          const token = document.cookie.replace(/(?:(?:^|.*;\s*)yourToken\s*=\s*([^;]*).*$)|^.*$/, "$1");
   #
   #          // Делаем запрос к бэкенду с токеном в заголовках
   #          const response = await fetch('user/users_all/da', {
   #              method: 'GET',
   #              headers: {
   #                  'Authorization': `Bearer ${token}`,
   #                  'Content-Type': 'application/json'
   #                  // Добавьте другие заголовки по необходимости
   #              }
   #          });
   #
   #          // Обрабатываем ответ по мере необходимости
   #          const data = await response.json();
   #          console.log(data);
   #      }
   #  </script>