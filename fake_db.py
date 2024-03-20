from faker import Faker
from Referral_system.models import Users, ReferralCode, ReferralRelationship
from datetime import datetime, timedelta
from random import random


faker = Faker(['en_US'])

for _ in range(20):
    fake_profile = faker.profile()
    Users.objects.create_user(username=fake_profile["username"],
                              password=faker.password(),
                              first_name=fake_profile["name"].split()[0],
                              last_name=fake_profile["name"].split()[1],
                              email=fake_profile['mail']
                              )

users = [id_['id'] for id_ in list(Users.objects.all().values("id"))]
for ind in range(20):
    user = users[ind-1]

    ReferralCode.objects.create(user_id=user,
                                code=faker.ean(length=13),
                                expiration_date=datetime.now() + timedelta(days=10),
                                is_active=faker.pybool()
                                )

list_code = [[code['id'], code['user_id']] for code in list(ReferralCode.objects.all().values("id", "user_id"))]
for ind in range(20):
    inviter = list_code[ind-1][1]
    invited = random.choice(users)
    refer_token = list_code[ind-1][0]

    ReferralRelationship.objects.create(inviter_id=inviter,
                                        invited_id=invited,
                                        refer_token_id=refer_token
                                        )