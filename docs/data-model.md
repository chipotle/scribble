# Models #

These are JSON-style document stores. The current database target is RethinkDB, although this could conceivably be backed by any comparable system.

## Users ##

	{
		"username": "chipotle",
		"display_name": "Watts Martin",
		"password": *bcrypted something*,
		"email": "layotl@gmail.com",
		"social": { "twitter": "chipotlecoyote", ... },
		"preferences": { ... },
		"following": [user1, user2, user3, ...],
		"subscriptions": [series1, series2, series3, ...]
	}

## Items ##

The *type* of an item may determine what properties it has. While many properties are common, a *series* item is the only one that has *contents* (which are other items, possibly including series) and *subscribers* (users who are notified when a new story is added to the series). A *text* item has versions. (We may want a cap on how many previous versions we'll store, depending on space limitations.)

Other item types can be pretty easily defined in this schema, with different characteristics. Image items might not need versioning, for instance, although perhaps they would. Comic strips/pages might go in a special "comic series" type which adds navigation buttons.

	{
		"title": "The Narrow Road in Morning Light",
		"slug": "narrow-road-in-morning-light",
		"author_id": *user_id*,
		"itemtype": "text",
		"kind": "story",
		"created_at": "2010-01-01",
		"updated_at": "2012-05-15",
		"genres": ["action", "fantasy"],
		"word_count": 6000,
		"likes": [user1, user2, user3, ...],
		"dislikes": [user1, user2, user3, ...],
		"views": 123,
		"bookmarks": [user1, user2, user3, ...],
		"tags": ["samurai", "wolf", "pretentious"],
		"versions": [
			{	"date": "2012-05-15",
				"text": "Lorem ipsum",
				"html": "<p>Lorem ipsum</p>" },
			{	"date": "2010-01-01",
				"text": "Lorem ipsum",
				"html": "<p>Lorem ipsum</p>" }
		],
		"description": { "text": "Lorem ipsum", "html": "<p>Lorem ipsum</p>" }
	},
	{
		"title": "A Gift of Fire, A Gift of Blood",
		"slug": "gift-of-fire-gift-of-blood",
		"author_id": *user_id*,
		"itemtype": "series",
		"kind": "novella",
		"created_at": "2010-01-01",
		"updated_at": "2012-05-15",
		"likes": [user1, user2, user3, ...],
		"dislikes": [user1, user2, user3, ...],
		"genres": ["romance", "fantasy", "horror"],
		"bookmarks": [user1, user2, user3, ...],
		"tags": ["bat", "ranea", "m/f"],
		"subscribers": [user1, user2, user3, ...],
		"contents": [item1, item2, item3, ...],
		"description": { "text": "Lorem ipsum", "html": "<p>Lorem ipsum</p>" }
	}
