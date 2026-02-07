# Chatbot Database Models with Timestamp Fields

## Overview
Created proper database models for chatbot functionality with proper timestamp fields following project standards.

## Models Created/Updated

### 1. Base Model (`src/models/base.py`)
- Created `TimestampMixin` class with standardized `created_at` and `updated_at` fields
- Provides consistent timestamp handling across all models

### 2. Conversation Model (`src/models/conversation.py`)
- Added `TimestampMixin` inheritance for consistent timestamp fields
- Maintains `user_id` foreign key for user isolation
- Has proper relationships with Message model
- Fields: `id`, `user_id`, `created_at`, `updated_at`

### 3. Message Model (`src/models/message.py`)
- Added `TimestampMixin` inheritance for consistent timestamp fields
- Maintains `conversation_id` and `user_id` foreign keys for relationships and user isolation
- Kept original `timestamp` field for message-specific timing
- Fields: `id`, `conversation_id`, `user_id`, `role`, `content`, `timestamp`, `created_at`, `updated_at`

### 4. Updated Existing Models
- Task model: Updated to use `TimestampMixin`
- User model: Updated to use `TimestampMixin`

## Timestamp Field Standards
- **Naming Convention**: `created_at` and `updated_at` (snake_case)
- **Data Type**: `datetime` with `Field(default_factory=datetime.utcnow)`
- **Indexing**: Both fields are indexed for performance
- **Immutability**: `created_at` is set once at creation
- **Auto-update**: `updated_at` is updated on record modifications (handled in service layer)

## Relationships
- Conversation ↔ Message (One-to-Many)
- User ↔ Conversation (One-to-Many)
- User ↔ Message (One-to-Many)
- User ↔ Task (One-to-Many)

## User Isolation
- All models include `user_id` field where appropriate for user data isolation
- Proper foreign key relationships established

## Service Layer Support
- Created `timestamp_service.py` with utilities for managing `updated_at` field updates
- Provides `update_model_updated_at()` function for automatic timestamp updates

## Migration Strategy
These changes maintain backward compatibility while adding the missing timestamp fields. The Message model now has both a `timestamp` field for message-specific timing and standard `created_at`/`updated_at` fields for general record tracking.