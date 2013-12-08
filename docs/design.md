## Goals ##

*a/k/a, "The job we hire Scribble to do"*

1. Present our stories in a pretty fashion. All of the existing solutions for this suck. They just do.
2. Let people give us both overall comments and specific critique.
3. Give us a "hub" for our creative works. We should have our own author home pages that can be moderately distinctive.
4. Give fans a way to follow their favorite authors and/or series.
5. Give fans a way to discover new stories they might like.

## Implied Requirements ##

* Good presentation templates.
* Theming set by the author.
* Follows of authors.
* Follows of series.
* Bookmarking individual stories.
* Comments on stories.
* Comments on individual *paragraphs* of stories.
* Document versioning (possibly).
* Like/dislike, Reddit style.
* A recommendation engine.
* A search engine.
* Metadata about genre, category, rating, etc.
* Analytics for our stories.

And, if we want to "beat" Fur Affinity in the category of "ease of finding other things we might like," it means we need to be able to get from something we're assumed to like---a new story by an author we follow, for instance---to stuff we'll *probably* like, such as a list of stories, series or authors bookmarked by fans of people we're fans of, in three clicks or less.

## Dashboard ##

So when we log in we should get a dashboard like Tumblr's which *immediately* starts out with the new stuff from people we're following (or if we're not following anyone, a suggestion for people to follow, a search box, some such). The sidebar gives us links to our followers/following lists, preferences, popular posts, recommendations.


## User Page ##

Our author's home page should have some customizability: themes and various blocks we can enable and *possibly* arrange. (That might be a post-launch thing.) Imagine something like this:

| Main Column	| Sidebar	|  
| :----------------:	| :---------:	|  
| Title Block	| Link List	|  
| Description	| Twitter	|  
| Featured Submission	| Bio	|  
| *x* Newest Submissions	| Favorites	|  
| Series List	|	|  
| Submission List	| Feeds	|  
[User Page]

## Story Uploading ##

Scribble is going to be written to use Markdown as its native format; enough people know it---even if they don't *know* they know it---to make that a credible approach. Ideally, we should be able to convert from HTML and BBCode to Markdown and *maybe* to import from Google Docs or other services. Converting from RTF is a noble goal but may have to go on the back burner.

Figuring out how to address document encoding would be a biggie, though. This repository looks like it might have the key to the problem (if we stick to PHP): <https://github.com/neitanod/forceutf8>

We may want to do document versioning, or at least allow that as a possibility.

## Story Downloading ##

This should be possible, using Pandoc behind the scenes to allow downloading in multiple forms. This might be something that authors get to allow/deny in preferences, too. Series should be able to be downloaded in ePub as single books with each story as a chapter or unit.

## Series/Story Management ##

Adding, removing, and re-ordering stories in series should be drag and drop (with some kind of non-JS fallback).
